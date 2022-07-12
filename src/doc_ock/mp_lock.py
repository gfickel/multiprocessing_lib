import os
import pickle
import time
import logging
from multiprocessing import Pool, Lock

import numpy as np

from doc_ock.utils import validate_inputs


def _proc_function(data_list, process, save_callback, out_path, save_batch):
    def save(data_name, results):
        with lock:
            if save_callback is not None:
                save_callback(f'{out_path}/data', results, data_name)
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

    try:
        data_name, results = [], []
        # last_save = time.time()
        final_data_list = discard_processed(data_list)

        for idx, curr_data in enumerate(final_data_list):
            print(f'Processing {idx}/{len(final_data_list)}...', end='\r')
            res = process(curr_data)
            data_name.append(curr_data)
            results.append(res)

            if len(data_name) > save_batch:  # or time.time()-last_save > 10:
                save(data_name, results)
                data_name, results = [], []
                last_save = time.time()

        if len(data_name) > 0:
            save(data_name, results)
    except BaseException as e:
        logging.error(str(e), exc_info=True)
        raise e

def _init(l):
    # https://stackoverflow.com/a/25558333/2704783
    global lock
    lock = l

def mp_lock(data_list, process, save_callback, num_procs, out_path, save_batch=10):
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
    save_callback : func
        Saving function callback that will receive the results from process. Must
        be declared with the following arguments:
        def save_callback(output_filepath, data_results, data_names)
            output_filepath : str
                Filename to save the results
            data_results : list
                A list of results from process function
            data_names : list
                A list of data names (instances from data_list)
    num_procs : int
        Number of processes to use
    out_path : str
        Output path
    save_batch : int
        Max number of results to group before saving
    """
    validate_inputs(data_list, process, save_callback, num_procs, out_path, save_batch)
    # This lock will be shared with all the processes
    lock = Lock()

    data_split = np.array_split(data_list, num_procs)
    args = [(data, process, save_callback, out_path, save_batch) for data in data_split]

    os.makedirs(out_path, exist_ok=True)
    os.makedirs(os.path.join(out_path, 'data'), exist_ok=True)
    with Pool(processes=num_procs, initializer=_init, initargs=(lock,)) as pool:
        pool.starmap(_proc_function, args)
