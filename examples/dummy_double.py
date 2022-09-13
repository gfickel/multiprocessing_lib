import argparse
import glob
import time

# from doc_ock.mp_lock import mp_lock
import sys
sys.path.append("../src/")
from doc_ock.mp_lock import mp_lock


def process(value, shared_dict):
    # print("A:", value, shared_dict["something"])
    time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script dummy')
    parser.add_argument('--num_procs', type=int, required=True,
            help='Number of processes')
    args = parser.parse_args()

    data_list = ["foo"+str(i) for i in range(11)]

    print("A")
    shared_dict = {
        "something": "foo"
    }
    mp_lock(data_list, process, None, args.num_procs, "dummy_out", shared_dict)

    print("B")
    # TODO: should we add something to make several mp_lock in parallel?
    data_list = ["bar"+str(i) for i in range(9)]
    shared_dict = {
        "something": "bar"
    }
    mp_lock(data_list, process, None, args.num_procs, "dummy_out2", shared_dict)