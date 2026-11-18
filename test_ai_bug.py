# 함정 실험: bug3_logic.py 의 find_max 만 보고 작성
import pytest
from bug3_logic import find_max


def test_find_max_basic():
    assert find_max([70, 85, 60, 95]) == 95


def test_find_max_ascending():
    assert find_max([10, 20, 30]) == 30


def test_find_max_single():
    assert find_max([5]) == 5


def test_find_max_negative():
    assert find_max([-3, -1, -2]) == -1


def test_find_max_empty_raises():
    with pytest.raises(IndexError):
        find_max([])
