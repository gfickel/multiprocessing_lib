import argparse
import glob
import time

# from doc_ock.mp_lock import mp_lock
import sys
sys.path.append("../src/")
from doc_ock.mp_lock import mp_lock


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script dummy')
    parser.add_argument('--num_procs', type=int, required=True,
            help='Number of processes')
    args = parser.parse_args()

    data_list = [str(i) for i in range(1000)]

    def process(im_path):
        # print("AAAAA")
        time.sleep(0.1)

    mp_lock(data_list, process, None, args.num_procs, "dummy_out")
