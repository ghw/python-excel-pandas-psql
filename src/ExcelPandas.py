import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import xlrd
import pandas as pd
from src.general.DirFunc import DirFunc
from src.general.PandasFunc import PandasFunc

dir_func = DirFunc()
pd_func = PandasFunc()


class ExcelPandas(object):

	def __init__(self):
		pass

	def get_sheet_names_from_excel_file(self, file=None):
		excel_file = xlrd.open_workbook(file, on_demand=True)
		return excel_file.sheet_names()

	def get_dataframe_from_excel_file(self, file=None, sheet_name=None, skip_rows_list=None):
		if sheet_name is None: sheet_name = 0  # if not specified, get first sheet
		if skip_rows_list is None: skip_rows_list = []

		df = pd.read_excel(file, sheet_name=sheet_name, encoding='utf-8', skiprows=skip_rows_list)
		return df

	def send_dataframe_to_excel_file(self, file=None,
									 dataframe_to_sheet_name_tuple_list=None,
									 write_index=None):
		if write_index is None: write_index = False
		if file is None: return

		folder = dir_func.get_file_location(file=file)
		if folder in [None, '']:
			folder = os.getcwd()
			file = os.path.join(folder, file)

		if not dir_func.exists_folder(folder):
			os.makedirs(folder)

		writer = pd.ExcelWriter(file, engine='xlsxwriter', options={'strings_to_urls': False})
		for df, sheet in dataframe_to_sheet_name_tuple_list:
			if pd_func.get_row_count_from_dataframe(df) == 0:
				continue
			df.to_excel(writer, sheet_name=sheet, index=write_index)
		writer.save()
		return
