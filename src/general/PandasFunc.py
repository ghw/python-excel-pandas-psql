import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np


class PandasFunc(object):

	def __init__(self):
		pass

	def get_row_count_from_dataframe(self, dataframe=None):
		return len(dataframe.index)