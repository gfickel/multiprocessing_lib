import unittest
import shutil
import os

from doc_ock.mp_dist import mp_dist
from doc_ock.mp_lock import mp_lock, mp_lock_batch
from doc_ock.mp_queue import mp_queue

TEST_PATH = 'tests/data/tmp/'


def compute_sum_squared(data, shared_data={}):
    return int(data)*int(data)

def compute_sum_squared_batch(data_list, shared_data={}):
    return [compute_sum_squared(x) for x in data_list]

def save_callback(out_filepath, results, names):
    with open(os.path.join(TEST_PATH, 'data.txt'), 'at') as fid:
        fid.write(str(sum(results))+'\n')

def run_sum_squared_test(mp_fun, data, num_procs, save_batch, batch=1):
    shutil.rmtree(TEST_PATH, ignore_errors=True)
    if batch == 1:
        mp_fun(data, compute_sum_squared, save_callback, num_procs,
               TEST_PATH, save_batch=save_batch)
    else:
        mp_fun(data, compute_sum_squared_batch, save_callback, num_procs,
               TEST_PATH, save_batch=save_batch, batch_size=batch)
    with open(os.path.join(TEST_PATH, 'data.txt'), 'rt') as fid:
        res = [int(x.strip()) for x in fid.readlines()]
    return sum(res)


class Correctness(unittest.TestCase):

    data = [str(x) for x in range(10)]

    def test_mp_dist(self):
        for num_procs in [1,2,3,4,5,6,7,8,16]:
            for save_batch in [1,2,3,4,5,6,50]:
                res = run_sum_squared_test(mp_dist, self.data, num_procs, save_batch)
                self.assertEqual(res, 285)

    def test_mp_lock(self):
        for num_procs in [1,2,3,4,5,6,7,8,16]:
            for save_batch in [1,2,3,4,5,6,50]:
                res = run_sum_squared_test(mp_lock, self.data, num_procs, save_batch)
                self.assertEqual(res, 285)

    def test_mp_queue(self):
        for num_procs in [1,2,3,4,5,6,7,8,16]:
            for save_batch in [1,2,3,4,5,6,50]:
                res = run_sum_squared_test(mp_queue, self.data, num_procs, save_batch)
                self.assertEqual(res, 285)

    def test_mp_lock_batch(self):
        for num_procs in [1,2,3,4,5,6,7,8,16]:
            for save_batch in [1,2,3,4,5,6,50]:
                for process_batch in [2, 4, 7, 15]:
                    res = run_sum_squared_test(
                        mp_lock_batch, self.data, num_procs, save_batch,
                        process_batch)
                    self.assertEqual(res, 285)