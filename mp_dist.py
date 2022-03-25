import os
import pickle
import time
from multiprocessing import Pool

import numpy as np


def _proc_function(data_list, proc_id, process, save_callback, out_path, save_batch):
    def save(data_name, results):
        if save_callback is not None:
            save_callback(f'{out_path}/data_{proc_id}.pickle', results, data_name)
        with open(f'{out_path}/processed_list_{proc_id}.txt', 'at') as fid:
            fid.write('\n'.join(data_name)+'\n')

    def discard_processed(data_list):
        try:
            with open(f'{out_path}/processed_list_{proc_id}.txt', 'rt') as fid:
                processed = [x.strip() for x in fid.readlines()]
        except:
            processed = []
        return list(set(data_list)-set(processed))

    os.makedirs(out_path, exist_ok=True)
    data_name, results = [], []
    last_save = time.time()
    final_data_list = discard_processed(data_list)

    for idx, curr_data in enumerate(final_data_list):
        print(f'Processing {idx}/{len(final_data_list)}...', end='\r')
        res = process(curr_data)
        data_name.append(curr_data)
        results.append(res)

        if len(data_name) > save_batch or time.time()-last_save > 2:
            save(data_name, results)
            data_name, results = [], []
            last_save = time.time()

    if len(data_name) > 0:
        save(data_name, results)

def mp_dist(data_list, process, save_callback, num_procs, out_path, save_batch=50):
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
    data_split = np.array_split(data_list, num_procs)
    args = [(data, idx, process, save_callback, out_path, save_batch)
            for idx,data in enumerate(data_split)]

    with Pool(processes=num_procs) as pool:
        pool.starmap(_proc_function, args)
