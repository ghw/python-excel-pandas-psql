import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import pandas as pd
import itertools

from src.general.StrFunc import StrFunc

str_func = StrFunc()


class PandasFunc(object):

	def __init__(self):
		pass

	def get_row_count_from_dataframe(self, dataframe=None):
		return len(dataframe.index)

	def get_dictionary_from_two_dataframe_columns(self, dataframe=None, key_column=None, value_column=None):
		return pd.Series(dataframe[value_column].values, index=dataframe[key_column]).to_dict()

	def get_dataframe_with_all_permutations_from_dict_with_list_values(self, dict_with_list_values=None):
		df = pd.DataFrame(list(
			itertools.product(*dict_with_list_values.values())
		), columns=dict_with_list_values.keys())
		return df

	def set_column_as_index(self, dataframe=None, column_name=None, drop_original_column=None):
		if drop_original_column is None: drop_original_column = False
		dataframe.reset_index(drop=True, inplace=True)
		dataframe.set_index(column_name, inplace=True, drop=drop_original_column)

	def get_dict_of_column_name_to_type_from_dataframe(self, dataframe=None):
		column_name_type_dict = dataframe.dtypes.apply(lambda x: x.name).to_dict()
		return column_name_type_dict

	def get_column_names_by_type(self, dataframe=None, column_dtype=None):
		column_name_type_dict = self.get_dict_of_column_name_to_type_from_dataframe(dataframe=dataframe)
		matched_columns = [k for k, v in column_name_type_dict.items()
						   if str(v).lower() == column_dtype.lower()]
		return matched_columns

	def contains_all_integer_in_float_column(self, dataframe=None, column_name=None):
		column_values = dataframe[column_name].values.copy()
		column_values = column_values[~np.isnan(column_values)]
		return np.array_equal(column_values, column_values.astype(int))

	def set_column_names_to_alpha_numeric(self, dataframe=None):
		columns_as_alpha_numeric = list(map(str_func.text_to_alpha_numeric, dataframe.columns))
		dataframe.columns = columns_as_alpha_numeric

	def set_column_names_to_snake_case(self, dataframe=None):
		columns_as_snake_case = list(map(str_func.text_to_snake_case, dataframe.columns))
		dataframe.columns = columns_as_snake_case

	def exists_unnamed_headers(self, dataframe=None):
		return any('unnamed' in col.lower() for col in dataframe.columns)

	def exists_column(self, dataframe=None, column_name=None):
		return column_name in dataframe.columns

	def get_length_of_dtype_object(self, object_value=None):
		try:
			return len(object_value)
		except:
			return 1

	def get_maximum_length_of_dtype_object_values(self, dataframe=None, column_name=None):
		return dataframe[column_name].map(lambda x: self.get_length_of_dtype_object(x)).max()
