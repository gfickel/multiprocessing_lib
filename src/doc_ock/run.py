from collections import defaultdict

import numpy as np

from benchmark import benchmark
from dot_dict import DefaultDotDict


def write_results(results, args):
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
    DATA_SIZE = 2096
    NUM_RUNS = 5

    for batch in BATCH:
        for process_time in PROCESS_TIME:
            res_list = defaultdict(lambda: defaultdict(list))
            for result_size in RESULT_SIZE:
                for rep in range(NUM_RUNS):
                    args = DefaultDotDict({
                        'num_procs': 16,
                        'result_size': result_size,
                        'process_time': process_time,
                        'process_time_jitter': 0,
                        'data_size': DATA_SIZE,
                        'save_batch': batch,
                        'out_path': '/mnt/disks/sdc/test_multiprocess/',
                    })
                    bench_res = benchmark(args)
                    for method, val in bench_res.items():
                        res_list[result_size][method].append(val)

            final_results = defaultdict(lambda: defaultdict(float))
            for key in res_list:
                for method, vals in res_list[key].items():
                    final_results[key][method] = np.median(vals)

            write_results(final_results, args)
