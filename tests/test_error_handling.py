import unittest
import pytest
import shutil

from doc_ock.mp_dist import mp_dist
from doc_ock.mp_lock import mp_lock
from doc_ock.mp_queue import mp_queue


def invalid_process(data):
    import invalid_module
    return 1


class ErrorHandling(unittest.TestCase):

    data = [str(x) for x in range(10)]

    def test_mp_dist(self):
        with pytest.raises(ModuleNotFoundError):
            mp_dist(self.data, invalid_process, None, 2, 'data/tmp/', 2)

    def test_mp_lock(self):
        with pytest.raises(ModuleNotFoundError):
            mp_lock(self.data, invalid_process, None, 2, 'data/tmp/', 2)

    def test_mp_queue(self):
        with pytest.raises(ModuleNotFoundError):
            mp_queue(self.data, invalid_process, None, 2, 'data/tmp/', 2)
