import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.general.DirFunc import DirFunc as DirFunc

dir_func = DirFunc()


def test_get_file_location():
	assert dir_func.get_file_location(
		file=os.path.join('test', 'test_folder', 'file_in_folder_1.log')
	) == os.path.join('test', 'test_folder')


def test_get_base_name_from_file():
	assert dir_func.get_base_name_from_file(
		file=os.path.join('test_folder', 'file_in_folder_1.log')
	) == 'file_in_folder_1'


def test_get_extension_from_file():
	assert dir_func.get_file_extension(
		file=os.path.join('test_folder', 'file_in_folder_1.log')
	) == '.log'


def test_exists_folder_where_exists():
	assert dir_func.exists_folder(
		folder=os.path.join(os.path.dirname(__file__), 'test_folder')
	) == True


def test_exists_folder_where_doesnot_exist():
	assert dir_func.exists_folder(
		folder=os.path.join(os.path.dirname(__file__), 'no_test_folder')
	) == False


def test_removing_temp_files():
	assert dir_func.remove_temporary_files(
		file_list=['~$abc.xlsx', 'abc.xlsx']
	).sort() == [
		'abc.xlsx'
	].sort()


def test_get_all_files_nonrecursive():
	assert dir_func.get_all_files_from_path(
		folder_path=os.path.join(os.path.dirname(__file__), 'test_folder'),
		pattern='*.log',
		recursive=False
	).sort() == [
		os.path.join(os.path.dirname(__file__), 'test_folder', 'file_in_folder_1.log')
	].sort()


def test_get_all_files_recursive():
	assert dir_func.get_all_files_from_path(
		folder_path=os.path.join(os.path.dirname(__file__), 'test_folder'),
		pattern='*.log',
		recursive=True
	).sort() == [
		os.path.join(os.path.dirname(__file__), 'test_folder', 'file_in_folder_1.log'),
		os.path.join(os.path.dirname(__file__), 'test_folder', 'test_subfolder', 'file_in_subfolder_1.log'),
		os.path.join(os.path.dirname(__file__), 'test_folder', 'test_subfolder', 'file_in_subfolder_2.log')
	].sort()


def test_get_latest_file():
	assert dir_func.get_latest_file(
		folder_path=os.path.join(os.path.dirname(__file__), 'test_folder'),
		pattern='*.log'
	) == os.path.join(os.path.dirname(__file__), 'test_folder', 'file_in_folder_1.log')


# def get_all_files_from_path(self, folder_path=None, pattern=None, recursive=None):
#
# def get_latest_file(self, folder_path=None, pattern=None):
#
# def get_abs_path(self, path=None):
#
# def get_full_abs_path(self, folder_path=None, filename=None):
