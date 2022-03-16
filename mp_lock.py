import os
import pickle
from multiprocessing import Pool, Lock

import numpy as np


def _proc_function(data_list, process, out_path, save_batch):
    def save(data_name, results):
        with lock:
            with open(f'{out_path}/data.pickle', 'ba+') as fid:
                pickle.dump({'data_name': data_name, 'results': results}, fid)
            with open(f'{out_path}/processed_list.txt', 'at') as fid:
                fid.write('\n'.join(data_name)+'\n')

    def discard_processed(data_list):
        with lock:
            try:
                with open(f'{out_path}/processed_list.txt', 'rt') as fid:
                    processed = [x.strip() for x in fid.readlines()]
            except:
                processed = []
        return list(set(data_list)-set(processed))

    os.makedirs(out_path, exist_ok=True)
    data_name, results = [], []
    final_data_list = discard_processed(data_list)

    for idx, curr_data in enumerate(final_data_list):
        print(f'Processing {idx}/{len(final_data_list)}...', end='\r')
        res = process(curr_data)
        if save_batch > 1:
            data_name.append(curr_data)
            results.append(res)

            if idx%10 == 0:
                save(data_name, results)
                data_name, results = [], []
        else:
            save(curr_data, res)

    if len(data_name) > 0:
        save(data_name, results)

def _init(l):
    # https://stackoverflow.com/a/25558333/2704783
    global lock
    lock = l

def mp_lock(data_list, process, num_procs, out_path, save_batch):
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
    # This lock will be shared with all the processes
    lock = Lock()

    data_split = np.array_split(data_list, num_procs)
    args = [(data, process, out_path, save_batch) for data in data_split]

    with Pool(processes=num_procs, initializer=_init, initargs=(lock,)) as pool:
        pool.starmap(_proc_function, args)
