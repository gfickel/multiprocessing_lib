import unittest
import pytest
import shutil

from doc_ock.mp_dist import mp_dist
from doc_ock.mp_lock import mp_lock
from doc_ock.mp_queue import mp_queue
from doc_ock.utils import InvalidArgumentsError


def invalid_process(data):
    import invalid_module
    return 1


class ErrorHandling(unittest.TestCase):

    data = [str(x) for x in range(10)]

    def test_mp_dist_user_exception(self):
        with pytest.raises(ModuleNotFoundError):
            mp_dist(self.data, invalid_process, None, 2, 'data/tmp/', 2)

    def test_mp_lock_user_exception(self):
        with pytest.raises(ModuleNotFoundError):
            mp_lock(self.data, invalid_process, None, 2, 'data/tmp/', 2)

    def test_mp_queue_user_exception(self):
        with pytest.raises(ModuleNotFoundError):
            mp_queue(self.data, invalid_process, None, 2, 'data/tmp/', 2)

    def test_mp_dist_invalid_data_list(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist([], invalid_process, None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid data_list' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist(None, invalid_process, None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid data_list' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist('element', invalid_process, None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid data_list' in str(e))

    def test_mp_lock_invalid_data_list(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock([], invalid_process, None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid data_list' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock(None, invalid_process, None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid data_list' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock('element', invalid_process, None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid data_list' in str(e))

    def test_mp_queue_invalid_data_list(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue([], invalid_process, None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid data_list' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue(None, invalid_process, None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid data_list' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue('element', invalid_process, None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid data_list' in str(e))

    def test_mp_dist_invalid_process(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist(self.data, None, None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid process' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist(self.data, 'fun', None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid process' in str(e))

    def test_mp_lock_invalid_process(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock(self.data, None, None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid process' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock(self.data, 'fun', None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid process' in str(e))

    def test_mp_queue_invalid_process(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue(self.data, None, None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid process' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue(self.data, 'fun', None, 2, 'data/tmp/', 2)
            self.assertTrue('Invalid process' in str(e))

    def test_mp_dist_invalid_num_procs(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist(self.data, invalid_process, None, 0, 'data/tmp/', 2)
            self.assertTrue('Invalid num_procs' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist(self.data, invalid_process, None, 1.2, 'data/tmp/', 2)
            self.assertTrue('Invalid num_procs' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist(self.data, invalid_process, None, -2, 'data/tmp/', 2)
            self.assertTrue('Invalid num_procs' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist(self.data, invalid_process, None, '2', 'data/tmp/', 2)
            self.assertTrue('Invalid num_procs' in str(e))

    def test_mp_lock_invalid_num_procs(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock(self.data, invalid_process, None, 0, 'data/tmp/', 2)
            self.assertTrue('Invalid num_procs' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock(self.data, invalid_process, None, 1.2, 'data/tmp/', 2)
            self.assertTrue('Invalid num_procs' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock(self.data, invalid_process, None, -2, 'data/tmp/', 2)
            self.assertTrue('Invalid num_procs' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock(self.data, invalid_process, None, '2', 'data/tmp/', 2)
            self.assertTrue('Invalid num_procs' in str(e))

    def test_mp_queue_invalid_num_procs(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue(self.data, invalid_process, None, 0, 'data/tmp/', 2)
            self.assertTrue('Invalid num_procs' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue(self.data, invalid_process, None, 1.2, 'data/tmp/', 2)
            self.assertTrue('Invalid num_procs' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue(self.data, invalid_process, None, -2, 'data/tmp/', 2)
            self.assertTrue('Invalid num_procs' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue(self.data, invalid_process, None, '2', 'data/tmp/', 2)
            self.assertTrue('Invalid num_procs' in str(e))

    def test_mp_dist_invalid_out_path(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist(self.data, invalid_process, None, 2, '', 2)
            self.assertTrue('Invalid out_path' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist(self.data, invalid_process, None, 2, None, 2)
            self.assertTrue('Invalid out_path' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist(self.data, invalid_process, None, 2, 234, 2)
            self.assertTrue('Invalid out_path' in str(e))

    def test_mp_lock_invalid_out_path(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock(self.data, invalid_process, None, 2, '', 2)
            self.assertTrue('Invalid out_path' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock(self.data, invalid_process, None, 2, None, 2)
            self.assertTrue('Invalid out_path' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock(self.data, invalid_process, None, 2, 234, 2)
            self.assertTrue('Invalid out_path' in str(e))

    def test_mp_queue_invalid_out_path(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue(self.data, invalid_process, None, 2, '', 2)
            self.assertTrue('Invalid out_path' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue(self.data, invalid_process, None, 2, None, 2)
            self.assertTrue('Invalid out_path' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue(self.data, invalid_process, None, 2, 234, 2)
            self.assertTrue('Invalid out_path' in str(e))

    def test_mp_dist_invalid_save_batch(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist(self.data, invalid_process, None, 2, 'data/tmp/', 0)
            self.assertTrue('Invalid save_batch' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist(self.data, invalid_process, None, 2, 'data/tmp/', 2.2)
            self.assertTrue('Invalid save_batch' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist(self.data, invalid_process, None, 2, 'data/tmp/', -4)
            self.assertTrue('Invalid save_batch' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_dist(self.data, invalid_process, None, 2, 'data/tmp/', None)
            self.assertTrue('Invalid save_batch' in str(e))

    def test_mp_lock_invalid_save_batch(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock(self.data, invalid_process, None, 2, 'data/tmp/', 0)
            self.assertTrue('Invalid save_batch' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock(self.data, invalid_process, None, 2, 'data/tmp/', 2.2)
            self.assertTrue('Invalid save_batch' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock(self.data, invalid_process, None, 2, 'data/tmp/', -4)
            self.assertTrue('Invalid save_batch' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_lock(self.data, invalid_process, None, 2, 'data/tmp/', None)
            self.assertTrue('Invalid save_batch' in str(e))

    def test_mp_queue_invalid_save_batch(self):
        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue(self.data, invalid_process, None, 2, 'data/tmp/', 0)
            self.assertTrue('Invalid save_batch' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue(self.data, invalid_process, None, 2, 'data/tmp/', 2.2)
            self.assertTrue('Invalid save_batch' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue(self.data, invalid_process, None, 2, 'data/tmp/', -4)
            self.assertTrue('Invalid save_batch' in str(e))

        with pytest.raises(InvalidArgumentsError) as e:
            mp_queue(self.data, invalid_process, None, 2, 'data/tmp/', None)
            self.assertTrue('Invalid save_batch' in str(e))
