import time
import random
import argparse
import shutil

import numpy as np

from mp_lock import mp_lock
from mp_queue import mp_queue


# Using global variables to configure our processing function
g_result_size, g_process_time, g_process_time_jitter = 0, 0, 0

def get_args():
    parser = argparse.ArgumentParser(description='Benchmark')
    parser.add_argument('--num_procs', type=int, required=True,
            help='Number of processes')
    parser.add_argument('--result_size', type=int, required=True,
            help='Processing result size in KBs')
    parser.add_argument('--process_time', type=float, required=True,
            help='How many milliseconds should the processing function take')
    parser.add_argument('--process_time_jitter', type=float, required=True,
            help='How many milliseconds of jitter to processing time')
    parser.add_argument('--data_size', type=int, required=True,
            help='Number of elements to process')
    parser.add_argument('--save_batch', type=int, required=True,
            help='How many elements to group before saving them')
    parser.add_argument('--out_path', type=str, required=True,
            help='Output path')
    return parser.parse_args()


def process(data):
    global g_result_size, g_process_time, g_process_time_jitter
    begin = time.time()
    dummy = 1
    element_size = max(1, int(np.sqrt(g_result_size*1024)))
    jitter = (1-random.random()*2)*g_process_time_jitter
    total_time_ms = max(0, g_process_time+jitter)
    while time.time()-begin < total_time_ms/1000:
        dummy = dummy+1
    return np.zeros((element_size, element_size), dtype=np.uint8)


def benchmark(args=None):
    global g_result_size, g_process_time, g_process_time_jitter
    if args is None:
        args = get_args()

    g_result_size = args.result_size
    g_process_time = args.process_time
    g_process_time_jitter = args.process_time_jitter
    results = {}
    data_list = [str(idx) for idx in range(args.data_size)]

    try:
        shutil.rmtree(args.out_path)
    except:
        pass
    start_time = time.time()
    mp_lock(data_list, process, args.num_procs, args.out_path, args.save_batch)
    results['mp_lock'] = (time.time()-start_time)*1000

    shutil.rmtree(args.out_path)
    start_time = time.time()
    mp_queue(data_list, process, args.num_procs, args.out_path, args.save_batch)
    results['mp_queue'] = (time.time()-start_time)*1000

    return results


if __name__ == '__main__':
    benchmark()

