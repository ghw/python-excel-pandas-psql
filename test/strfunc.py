import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.general.StrFunc import StrFunc as StrFunc

str_func = StrFunc()


def test_001_is_camel_case_where_small_camel_case():
	assert str_func.is_camel_case('smallcamelCase') == True


def test_002_is_camel_case_where_capital_camel_case():
	assert str_func.is_camel_case('CapitalcamelCase') == True


def test_003_is_camel_case_where_snake_case():
	assert str_func.is_camel_case('snake_CASE') == False


def test_004_is_camel_case_where_linebreak():
	assert str_func.is_camel_case('''line\nbreak''') == False


def test_005_is_camel_case_where_spaces():
	assert str_func.is_camel_case('''spaces in text''') == False


def test_006_is_camel_case_where_symbol():
	symbols = '''`~!@#$%^&*()-_=+[]{};':"\\|,./<>?'''
	for s in symbols:
		assert str_func.is_camel_case('''symbol{0}Found'''.format(s)) == False


def test_007_remove_accent_where_accented():
	accented_text = 'àèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÃÑÕäëïöüÄËÏÖÜŸçÇßØøÅåÆæœ'
	normal_text = 'aeiouAEIOUaeiouyAEIOUYaeiouAEIOUanoANOaeiouAEIOUYcCssOoAaAEaeoe'
	assert str_func.remove_accent(accented_text) == normal_text


def test_008_clean_snake_case():
	assert str_func.clean_snake_case('àbc__DÊF_') == 'abc_DEF_'


def test_009_to_alpha_numeric():
	assert str_func.text_to_alpha_numeric('abc yyyy/mm/dd', replace_string='_') == 'abc_yyyy_mm_dd'


def test_010_text_to_camel_case_upper():
	assert str_func.text_to_camel_case('Àbc dêf', case='upper') == 'AbcDef'


def test_011_text_to_camel_case_lower():
	assert str_func.text_to_camel_case('Àbc dêf', case='lower') == 'abcDef'


def test_012_camel_case_to_snake_case_upper():
	assert str_func.camel_case_to_snake_case('abcDef', case='upper') == 'ABC_DEF'


def test_013_camel_case_to_snake_case_lower():
	assert str_func.camel_case_to_snake_case('AbcDef', case='lower') == 'abc_def'


def test_014_text_to_snake_case_from_camel():
	assert str_func.text_to_snake_case('abcDef', case='lower') == 'abc_def'


def test_015_text_to_snake_case_from_normal():
	assert str_func.text_to_snake_case('abc def yyyy/mm-dd 123', case='lower') == 'abc_def_yyyy_mm_dd_123'
