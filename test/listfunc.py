import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.general.ListFunc import ListFunc as ListFunc

list_func = ListFunc()

list_with_duplicates = [1, 1, 2, 3]
unique_list = [1, 2, 3]
list_one = [1, 2, 3, 4]
list_two = [2, 3, 4, 5]
list_common = [2, 3, 4]
list_union = [1, 2, 3, 4, 5]
list_of_lists = [[1, 2], [3, 4, 5]]
flattened_list = [1, 2, 3, 4, 5]


def test_001_get_unique_list():
	assert list_func.get_unique_list(list_with_duplicates, sorted=True, reversed=False) == unique_list


def test_002_get_common_items():
	assert list_func.get_common_items(list_one, list_two) == list_common


def test_003_get_all_items():
	assert list_func.get_all_items(list_one, list_two) == list_union


def test_004_get_flat_list():
	assert list_func.get_flat_list(list_of_lists) == flattened_list
