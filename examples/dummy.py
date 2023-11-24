import argparse
import random
import time

from doc_ock.mp_lock import mp_lock_value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script dummy')
    parser.add_argument('--num_procs', type=int, required=True,
            help='Number of processes')
    args = parser.parse_args()

    data_list = [str(i) for i in range(10)]

    def process(data, shared_data={}, init_values={}):
        time.sleep(random.random())
        return data

    vals = mp_lock_value(data_list, process, None, args.num_procs, "dummy_out", verbose=False)
    print(vals)
