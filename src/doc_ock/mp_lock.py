import os
import time
import logging
from contextlib import suppress
from typing import List, Callable
from contextlib import redirect_stdout
from multiprocessing import Pool, Lock

from tqdm import tqdm
import numpy as np

from doc_ock.utils import validate_inputs, save_results, load_results


def _discard_processed(data_list, out_path):
    processed = []
    with suppress(FileNotFoundError):
        with open(f'{out_path}/processed_list.txt', 'rt') as fid:
            processed = [x.strip() for x in fid.readlines()]

    return list(set(data_list)-set(processed))

def _proc_function(data_list, process, init_function, save_callback, out_path,
                   save_batch, shared_data, verbose, ith_process,
                   batch_processing=False):

    def save(data_name, results):
        with lock:
            if save_callback is not None:
                save_callback(f'{out_path}/data', results, data_name)
            with open(f'{out_path}/processed_list.txt', 'at') as fid:
                fid.write('\n'.join(data_name)+'\n')

    try:
        os.makedirs(out_path, exist_ok=True)
        data_name, results = [], []
        init_vals = {}
        if init_function is not None:
            init_vals = init_function(shared_data)

        if verbose:
            progress = tqdm(
                total=len(data_list),
                position=ith_process,
                desc=f'Process #{ith_process}'
            )
    
        # https://stackoverflow.com/questions/1154446/is-file-append-atomic-in-unix
        with open(f'{out_path}/user_output.txt', 'a') as fid:
            with redirect_stdout(fid):
                for idx, curr_data in enumerate(data_list):
                    res = process(curr_data, shared_data, init_vals)
                    if not batch_processing:
                        res, curr_data = [res], [curr_data]
                    data_name.extend(curr_data)
                    results.extend(res)

                    if len(data_name) > save_batch:  # or time.time()-last_save > 10:
                        save(data_name, results)
                        data_name, results = [], []
                        last_save = time.time()

                    if verbose: progress.update(1)

        if len(data_name) > 0:
            save(data_name, results)
    except BaseException as e:
        logging.error(str(e), exc_info=True)
        raise e

def _init(l):
    # https://stackoverflow.com/a/25558333/2704783
    global lock
    lock = l

def mp_lock(data_list: List[str], process: Callable, save_callback: Callable,
            num_procs: int, out_path: str, save_batch: int=10, shared_data: dict={},
            init_function: Callable=None, verbose: bool=True):
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
    shared_data : dict
        Data shared within all the processes
    init_function : Callable
        Function that is called once, for every process. Receives shared_data and
        their return values are passed to the process function
    """
    validate_inputs(data_list, process, save_callback, num_procs, out_path, save_batch)
    # This lock will be shared with all the processes
    lock = Lock()

    final_data_list = _discard_processed(data_list, out_path)
    data_split = np.array_split(final_data_list, num_procs)
    if verbose:
        print(f'Data splitted in {len(data_split)} slices.')

    with tqdm(total=len(data_list), disable=not verbose) as pbar:
        args = [(data, process, init_function, save_callback, out_path, save_batch,
                 shared_data, verbose, i) for i,data in enumerate(data_split)]
        with Pool(processes=num_procs, initializer=_init, initargs=(lock,)) as pool:
            pool.starmap(_proc_function, args)


def mp_lock_batch(data_list: List[str], process: Callable,
                  save_callback: Callable, num_procs: int, out_path: str,
                  batch_size: int, save_batch: int=10, shared_data: dict={},
                  init_function: Callable=None, verbose: bool=True):
    """ Given a list of data and a process function, runs it in parallel and save
    the results to out_path. This function saves all the intermediate calculation,
    so you can always resume it.

    Parameters
    ----------
    data_list : list(str)
        List of data to process. Can be a list of images, for example.
    batch_size : int
        Batch size to be processed
    process : func
        The processing function that gets a batch of elements from data_list, process
        them and returns a (pickable) value
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
    shared_data : dict
        Data shared within all the processes
    init_function : Callable
        Function that is called once, for every process. Receives shared_data and
        their return values are passed to the process function
    verbose : bool
        Controls tqdm output
    """
    validate_inputs(data_list, process, save_callback, num_procs, out_path, save_batch, batch_size)
    # This lock will be shared with all the processes
    lock = Lock()

    final_data_list = _discard_processed(data_list, out_path)
    group_data = [final_data_list[x:x+batch_size] for x in range(0, len(final_data_list), batch_size)]
    data_split = np.array_split(group_data, num_procs)
    if verbose:
        print(f'Data splitted in {len(data_split)}|{num_procs} slices of size {batch_size}')

    with tqdm(total=len(data_list), disable=not verbose) as pbar:
        args = [(data, process, init_function, save_callback, out_path, save_batch,
                 shared_data, verbose, i, True) for i,data in enumerate(data_split)]

        with Pool(processes=num_procs, initializer=_init, initargs=(lock,)) as pool:
            pool.starmap(_proc_function, args)



def mp_lock_value(data_list: List[str], process: Callable, save_callback: Callable,
            num_procs: int, out_path: str, save_batch: int=10, shared_data: dict={},
            init_function: Callable=None, verbose: bool=True):
    """ Given a list of data and a process function, runs it in parallel, save
    the results to out_path, and when it finishes it returns the results. This
    function saves all the intermediate calculation, so you can always resume it.

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
    shared_data : dict
        Data shared within all the processes
    init_function : Callable
        Function that is called once, for every process. Receives shared_data and
        their return values are passed to the process function
    verbose : bool
        Controls tqdm output

    Returns
    -------
    results_list : list()
        A list of results generated by process, and matching data_list order
    """
    global my_save_callback
    def my_save_callback(*kwargs):
        save_results(*kwargs)
        if save_callback is not None:
            save_callback(*kwargs)

    mp_lock(data_list, process, my_save_callback, num_procs, out_path,
            save_batch, shared_data, init_function, verbose)

    return load_results(data_list, out_path)
