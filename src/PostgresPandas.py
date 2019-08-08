import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import re
import io
import pandas as pd
from sqlalchemy import create_engine

from src.general.PandasFunc import PandasFunc

pd_func = PandasFunc()


class PostgresPandas(object):

	def __init__(self, host=None, database=None, username=None, password=None):
		self.host = host
		self.database = database
		self.username = username
		self.password = password

	def get_database_connectors(self):
		db_conn_string = 'postgresql://{0}:{1}@{2}/{3}'.format(
			self.username, self.password, self.host, self.database
		)
		engine = create_engine(db_conn_string)
		conn = engine.raw_connection()
		cur = conn.cursor()
		return engine, conn, cur

	def close_database_connectors(self, engine=None, conn=None, cur=None):
		conn.commit()
		cur.close()
		conn.close()
		return

	def get_psql_query_results_as_dataframe(self, query=None):
		engine, conn, cur = self.get_database_connectors()
		df = pd.read_sql_query(query, con=engine)
		self.close_database_connectors(engine, conn, cur)
		return df

	def send_dataframe_to_psql(self, dataframe=None, schema_name=None, table_name=None):
		if dataframe is None: return
		if table_name is None: return
		if schema_name is None: schema_name = 'public'

		engine, conn, cur = self.get_database_connectors()

		# general csv features
		csv_sep = '\t'
		csv_null_rep = '#N/A'

		# save dataframe as temp csv
		csv_io = io.StringIO()
		dataframe.to_csv(csv_io, sep=csv_sep, encoding='utf-8-sig',
						 header=False, index=False, na_rep=csv_null_rep)
		csv_contents = csv_io.getvalue()
		csv_contents = re.sub(r'NaT', csv_null_rep, csv_contents)
		csv_io.seek(0)
		csv_io.write(csv_contents)

		# copy from temp csv to psql table
		csv_io.seek(0)
		cur.copy_from(csv_io, '{0}.{1}'.format(schema_name, table_name),
					  columns=dataframe.columns.tolist(),
					  sep=csv_sep, null=csv_null_rep)
		csv_io.close()

		self.close_database_connectors(engine, conn, cur)
		return
