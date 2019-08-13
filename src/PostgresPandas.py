import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import re
import io
import pandas as pd
from sqlalchemy import create_engine

from src.general.PandasFunc import PandasFunc


class PostgresPandas(PandasFunc):
	null_identifier = {
		'int32': -1234567890,
		'int64': -1234567890,
		'general': '#N/A'
	}

	def __init__(self, host=None, database=None, username=None, password=None):
		super().__init__()
		self.host = host
		self.database = database
		self.username = username
		self.password = password

	def __get_database_connectors(self):
		db_conn_string = 'postgresql://{0}:{1}@{2}/{3}'.format(
			self.username, self.password, self.host, self.database
		)
		engine = create_engine(db_conn_string)
		conn = engine.raw_connection()
		cur = conn.cursor()
		return engine, conn, cur

	def __close_database_connectors(self, conn=None, cur=None):
		conn.commit()
		cur.close()
		conn.close()
		return

	def get_psql_query_results_as_dataframe(self, query=None):
		engine, conn, cur = self.__get_database_connectors()
		df = pd.read_sql_query(query, con=engine)
		self.__close_database_connectors(conn, cur)
		return df

	def send_dataframe_to_psql(self, dataframe=None, schema_name=None, table_name=None):
		if dataframe is None: return
		if table_name is None: return
		if schema_name is None: schema_name = 'public'

		dataframe_for_upload = dataframe.copy()

		self.__correct_float_columns(dataframe_for_upload)
		self.set_column_names_to_alpha_numeric(dataframe_for_upload)
		self.set_column_names_to_snake_case(dataframe_for_upload)
		self.__clean_delimiter_in_object_columns_from_dataframe(dataframe_for_upload)
		self.__create_table(
			schema_name=schema_name, table_name=table_name,
			column_name_type_dict=self.__get_dict_of_column_name_to_type_from_dataframe_for_psql(dataframe_for_upload)
		)

		self.__upload_dataframe_to_psql(dataframe=dataframe_for_upload, schema_name=schema_name, table_name=table_name)

		self.__update_null_in_columns(
			schema_name=schema_name, table_name=table_name,
			dataframe=dataframe_for_upload, column_dtype='int64'
		)
		self.__update_null_in_columns(
			schema_name=schema_name, table_name=table_name,
			dataframe=dataframe_for_upload, column_dtype='int32'
		)

		return

	def __upload_dataframe_to_psql(self, dataframe=None, schema_name=None, table_name=None):
		engine, conn, cur = self.__get_database_connectors()

		# general csv features
		csv_sep = '\t'

		# save dataframe as temp csv
		csv_io = io.StringIO()
		dataframe.to_csv(csv_io, sep=csv_sep, encoding='utf-8-sig',
						 header=False, index=False, na_rep=self.null_identifier['general'])
		csv_contents = csv_io.getvalue()
		csv_contents = re.sub(r'NaT', self.null_identifier['general'], csv_contents)
		csv_io.seek(0)
		csv_io.write(csv_contents)

		# copy from temp csv to psql table
		csv_io.seek(0)
		cur.copy_from(csv_io, '{0}.{1}'.format(schema_name, table_name),
					  columns=dataframe.columns.tolist(),
					  sep=csv_sep, null=self.null_identifier['general'])
		csv_io.close()

		self.__close_database_connectors(conn, cur)

		return

	def __get_psql_array_format_of_python_list(self, python_list=None):
		psql_array = '({0})'.format(str(python_list)[1:-1])
		return psql_array

	def __execute_query(self, query=None):
		engine, conn, cur = self.__get_database_connectors()
		cur.execute(query)
		self.__close_database_connectors(conn, cur)
		return

	def __drop_table(self, schema_name=None, table_name=None):
		del_command = 'DROP TABLE IF EXISTS {0}."{1}";'.format(schema_name, table_name)
		self.__execute_query(del_command)
		return

	def __create_table_as(self, query=None, schema_name=None, table_name=None):
		create_command = 'CREATE TABLE {0}."{1}" AS {2}'.format(schema_name, table_name, query)
		self.__execute_query(query=create_command)
		return

	def __create_table(self, schema_name=None, table_name=None, column_name_type_dict=None):
		column_types = ', '.join(['{0} {1}'.format(col_n, col_t)
								  for col_n, col_t in column_name_type_dict.items()])
		create_command = 'CREATE TABLE {0}."{1}" ({2});'.format(schema_name, table_name, column_types)
		self.__execute_query(query=create_command)
		return

	def __correct_float_columns(self, dataframe=None):
		float_32_column_list = self.get_column_names_by_type(dataframe=dataframe, column_dtype='float32')
		float_64_column_list = self.get_column_names_by_type(dataframe=dataframe, column_dtype='float64')
		float_column_list = float_32_column_list + float_64_column_list

		if len(float_column_list) == 0: return

		for float_col in float_column_list:
			if self.contains_all_integer_in_float_column(dataframe=dataframe, column_name=float_col):
				dataframe[float_col] = dataframe[float_col].fillna(self.null_identifier['int64']).astype(int)
		return

	def __get_dict_of_column_name_to_type_from_dataframe_for_psql(self, dataframe=None):
		pandas_dtype_to_psql_column_type_dict = {
			"int64": "int",
			"int32": "int",
			"float32": "decimal",
			"float64": "decimal",
			"datetime64[ns]": "timestamp",
			"bool": "boolean",
			"array[object]": "character varying(256)[]"
		}

		pandas_column_name_type_dict = self.get_dict_of_column_name_to_type_from_dataframe(dataframe)
		psql_column_name_type_dict = dict()

		for k, v in pandas_column_name_type_dict.items():
			if v != 'object':
				psql_column_name_type_dict[k] = pandas_dtype_to_psql_column_type_dict[v]
			else:
				max_number_of_characters = \
					self.get_maximum_length_of_dtype_object_values(dataframe=dataframe, column_name=k)
				if max_number_of_characters <= 2056:
					psql_column_name_type_dict[k] = 'character varying({})'.format(max_number_of_characters)
				else:
					psql_column_name_type_dict[k] = 'text'

		return psql_column_name_type_dict

	def __clean_delimiter_in_object_columns_from_dataframe(self, dataframe=None):
		object_column_list = self.get_column_names_by_type(dataframe=dataframe, column_dtype='object')
		for obj_col in object_column_list:
			dataframe[obj_col] = dataframe[obj_col].str. \
				replace('\t', ' ', regex=True). \
				replace('\r\n', '', regex=True). \
				replace('\n', '', regex=True). \
				replace('"', '\'', regex=True). \
				replace(',', '\|', regex=True)
		return
s
	def __update_null_in_columns(self, dataframe=None, column_dtype=None, schema_name=None, table_name=None):
		int_columns = self.get_column_names_by_type(dataframe=dataframe, column_dtype=column_dtype)
		if len(int_columns) < 1: return

		update_command = ''
		for int_col in int_columns:
			update_command += '''
	s			UPDATE {0}.{1}
				SET {2} = NULL
				WHERE {2} = {3};
				'''.format(schema_name, table_name, int_col, self.null_identifier[column_dtype])
		self.__execute_query(query=update_command)
		return
