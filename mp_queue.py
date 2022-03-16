import os
import pickle
import multiprocessing as mp 

import numpy as np


def listener(q, out_path):
    '''listens for messages on the q, writes to file. '''
    try:
        os.makedirs(out_path, exist_ok=True)
        with open(out_path+'/data.bin', 'wb+') as f:
            while 1:
                m = q.get()
                if m == 'kill':
                    break
                pickle.dump(m, f)
                # f.flush()
    except BaseException as e:
        import logging
        logging.error(str(e), exc_info=True)

def _proc_function(data_list, process, out_path, save_batch, q):
    data_name, results = [], []
    final_data_list = data_list

    for idx, curr_data in enumerate(final_data_list):
        print(f'Processing {idx}/{len(final_data_list)}...', end='\r')
        res = process(curr_data)
        if save_batch > 1:
            data_name.append(curr_data)
            results.append(res)

            if idx%10 == 0:
                q.put({'data_name': data_name, 'results': results})
                data_name, results = [], []
        else:
            q.put({'data_name': curr_data, 'results': res})

    if len(data_name) > 0:
        q.put({'data_name': data_name, 'results': results})

def _init(l):
    # https://stackoverflow.com/a/25558333/2704783
    global lock
    lock = l

def mp_queue(data_list, process, num_procs, out_path, save_batch):
    """ Given a list of data and a process function, runs it in parallel and save
    the results to out_path. This function saves all the intermediate calculation,
    so you can always resume it.

    Parameters
    ----------
    data_list : list(str)
        List of data to process. Can be a list of images, for example.
    process : func
        The processing function that gets an element from data_list, process it and
        returns a (pickable) value
    num_procs : int
        Number of processes to use
    out_path : str
        Output path
    save_batch : int
        Number of results to group before saving
    """
    #must use Manager queue here, or will not work
    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(num_procs)

    #put listener to work first
    watcher = pool.apply_async(listener, (q, out_path))

    #fire off workers
    data_split = np.array_split(data_list, num_procs)
    jobs = []
    for data in data_split:
        job = pool.apply_async(_proc_function, (data, process, out_path, save_batch, q))
        jobs.append(job)

    # collect results from the workers through the pool result queue
    for job in jobs:
        job.get()

    #now we are done, kill the listener
    q.put('kill')
    pool.close()
    pool.join()
