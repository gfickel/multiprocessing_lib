import time
import random
import argparse
import shutil
from collections import defaultdict

import numpy as np

from mp_lock import mp_lock
from mp_queue import mp_queue
from benchmark import benchmark
from dot_dict import DefaultDotDict


def write_results(results, args, result_size):
    with open('results.txt', 'a') as fid:
        tech_results = defaultdict(list)
        for result_size in results:
            for technique in results[result_size]:
                tech_results[technique].append(results[result_size][technique])


        for technique in tech_results:
            fid.write((f'{technique} - Batch {args.save_batch}, '
            f'Process Time {args.process_time}\n'))
            fid.write('\n'.join([f'{x:.2f}' for x in tech_results[technique]])+'\n')


if __name__ == '__main__':
    RESULT_SIZE = [1, 10, 100, 1000, 10000]
    BATCH = [1, 10, 50]
    PROCESS_TIME = [0, 25, 100, 500]

    for batch in BATCH:
        for process_time in PROCESS_TIME:
            res = defaultdict(dict)
            for result_size in RESULT_SIZE:
                args = DefaultDotDict({
                    'num_procs': 16,
                    'result_size': result_size,
                    'process_time': process_time,
                    'process_time_jitter': 0,
                    'data_size': 1024,
                    'save_batch': batch,
                    'out_path': 'test/',
                })
                res[result_size] = benchmark(args)
            write_results(res, args, result_size)
