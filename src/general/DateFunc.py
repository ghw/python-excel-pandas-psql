import pandas
from datetime import datetime


class DateFunc(object):

	def get_year(self, date_entity=None, date_format=None):
		if date_entity is None: return None
		if date_format is None: date_format = '%Y-%m-%d'

		if type(date_entity) in (datetime, pandas._libs.tslib.Timestamp):
			return date_entity.year

		if type(date_entity) == str:
			try:
				datetime.strptime(date_entity, date_format)
			except ValueError:
				raise ValueError("Date should be in the format {0}".format(date_format))

			year, month, day = date_entity.split("-")
			return int(year)

		return None

	def text_to_datetime(self, text=None, date_format=None):
		if type(text) == str:
			try:
				datetime_from_text = datetime.strptime(text, date_format)
				return datetime_from_text
			except ValueError:
				raise ValueError("Date should be in the format {0}".format(date_format))
		return None

	def get_difference_in_year(self, from_date=None, to_date=None, date_format=None):
		if from_date is None: return None

		if to_date is None:
			to_date = datetime.today()

		if type(from_date) not in (datetime, pandas._libs.tslib.Timestamp, str):
			return None
		if type(from_date) not in (datetime, pandas._libs.tslib.Timestamp, str):
			return None

		if type(from_date) == str:
			from_date = self.text_to_datetime(text=from_date, date_format=date_format)

		if type(to_date) == str:
			to_date = self.text_to_datetime(text=to_date, date_format=date_format)

		years_diff = to_date.year - from_date.year

		if to_date.month < from_date.month:
			years_diff -= 1
			return years_diff

		if to_date.month == from_date.month and to_date.day < from_date.day:
			years_diff -= 1
			return years_diff

		return years_diff
