import unittest
import shutil

from doc_ock.mp_dist import mp_dist
from doc_ock.mp_lock import mp_lock
from doc_ock.mp_queue import mp_queue


def compute_sum_squared(data):
    return int(data)*int(data)

def save_callback(out_filepath, results, names):
    with open('data/tmp/data.txt', 'at') as fid:
        fid.write(str(sum(results))+'\n')

def run_sum_squared_test(mp_fun, data, num_procs, batch_size):
    shutil.rmtree('data/tmp/', ignore_errors=True)
    mp_fun(data, compute_sum_squared, save_callback, num_procs, 'data/tmp/', batch_size)
    with open('data/tmp/data.txt', 'rt') as fid:
        res = [int(x.strip()) for x in fid.readlines()]
    return sum(res)


class Correctness(unittest.TestCase):

    data = [str(x) for x in range(10)]

    def test_mp_dist(self):
        for num_procs in [1,2,3,4,5,6,7,8]:
            for batch_size in [1,2,3,4,5,6]:
                res = run_sum_squared_test(mp_dist, self.data, num_procs, batch_size)
                self.assertEqual(res, 285)

    def test_mp_lock(self):
        for num_procs in [1,2,3,4,5,6,7,8]:
            for batch_size in [1,2,3,4,5,6]:
                res = run_sum_squared_test(mp_lock, self.data, num_procs, batch_size)
                self.assertEqual(res, 285)

    def test_mp_queue(self):
        for num_procs in [1,2,3,4,5,6,7,8]:
            for batch_size in [1,2,3,4,5,6]:
                res = run_sum_squared_test(mp_queue, self.data, num_procs, batch_size)
                self.assertEqual(res, 285)
