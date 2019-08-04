import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.general.DateFunc import DateFunc as DateFunc
import pytest
from datetime import datetime
import pandas as pd

date_func = DateFunc()

date_str = '2010-10-15'
date_str_correct_format = '%Y-%m-%d'
date_str_incorrect_format = '%Y-%d-%m'
date_datetime = datetime(year=2010, month=10, day=15)
date_pandas_timestamp = pd.Timestamp(2010, 10, 15)
date_year = 2010
future_date_datetime = datetime(year=2020, month=10, day=15)
future_date_early_month_datetime = datetime(year=2020, month=9, day=15)
future_date_early_day_datetime = datetime(year=2020, month=10, day=14)
future_date_pandas_timestamp = pd.Timestamp(2020, 10, 15)


def test_001_get_year_from_str_with_correct_format():
	assert date_func.get_year(date_entity=date_str) == date_year


def test_002_get_year_from_str_with_incorrect_format():
	with pytest.raises(ValueError, match=r'Date should be in the format *'):
		date_func.get_year(date_entity=date_str, date_format=date_str_incorrect_format)


def test_003_get_year_from_datetime():
	assert date_func.get_year(date_entity=date_datetime) == date_year


def test_004_get_year_from_pandas_timestamp():
	assert date_func.get_year(date_entity=date_pandas_timestamp) == date_year


def test_005_text_to_datetime_with_correct_format():
	assert date_func.text_to_datetime(text=date_str, date_format=date_str_correct_format) == date_datetime


def test_006_text_to_datetime_with_incorrect_format():
	with pytest.raises(ValueError, match=r'Date should be in the format *'):
		date_func.text_to_datetime(text=date_str, date_format=date_str_incorrect_format)


def test_007_get_difference_in_year_diff_year():
	assert date_func.get_difference_in_year(from_date=date_datetime, to_date=future_date_datetime) == 10


def test_008_get_difference_in_year_diff_year_early_month():
	assert date_func.get_difference_in_year(from_date=date_datetime, to_date=future_date_early_month_datetime) == 9


def test_009_get_difference_in_year_diff_year_same_month_early_day():
	assert date_func.get_difference_in_year(from_date=date_datetime, to_date=future_date_early_day_datetime) == 9


def test_010_get_difference_in_year_diff_year_pandas_timestamp():
	assert date_func.get_difference_in_year(from_date=date_datetime, to_date=future_date_pandas_timestamp) == 10


def test_011_get_difference_in_year_diff_year_str_correct_format():
	assert date_func.get_difference_in_year(from_date=date_datetime, to_date=date_str,
											date_format=date_str_correct_format) == 0


def test_012_get_difference_in_year_diff_year_str_incorrect_format():
	with pytest.raises(ValueError, match=r'Date should be in the format *'):
		date_func.get_difference_in_year(from_date=date_datetime, to_date=date_str,
										 date_format=date_str_incorrect_format)