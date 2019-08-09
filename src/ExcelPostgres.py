import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.ExcelPandas import ExcelPandas
from src.PostgresPandas import PostgresPandas


class ExcelPostgres(PostgresPandas):

	def __init__(self, host=None, database=None, username=None, password=None):
		super().__init__(host=host, database=database, username=username, password=password)
		self.excel_pandas = ExcelPandas()

	def get_psql_query_result_in_excel(self, dict_with_filepath_to_query_and_excel_sheet=None):
		"""
		:param dict_with_filepath_to_query_and_excel_sheet: should be in following format
		{
			<excel_file_path_as_string> : [
				{
					'query': <query>,
					'sheet': <sheet_name>
				},
				{
					'query': <query>,
					'sheet': <sheet_name>
				}
			]
		}
		"""
		for filepath, list_of_dicts_with_query_and_sheet in dict_with_filepath_to_query_and_excel_sheet.items():

			list_of_tuple_with_df_and_sheet = []
			for dict_with_query_and_sheetname in list_of_dicts_with_query_and_sheet:
				df = self.get_psql_query_results_as_dataframe(query=dict_with_query_and_sheetname['query'])
				list_of_tuple_with_df_and_sheet.append(df, dict_with_query_and_sheetname['sheet'])

			self.send_dataframe_to_excel_file(
				file=filepath, dataframe_to_sheet_name_tuple_list=list_of_tuple_with_df_and_sheet, write_index=False
			)

		return

	def send_excel_to_postgres(self, file=None, sheet_name=None, skip_rows_list=None,
							   schema_name=None, table_name=None):
		df = self.excel_pandas.get_dataframe_from_excel_file(
			file=file, sheet_name=sheet_name, skip_rows_list=skip_rows_list
		)
		if self.pd_func.get_row_count_from_dataframe(df) > 0:
			self.send_dataframe_to_psql(self, dataframe=df, schema_name=schema_name, table_name=table_name)
		return
