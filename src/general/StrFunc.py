import re
import unidecode


class StrFunc(object):

	def __init__(self):
		pass

	def is_camel_case(self, text=None):
		if text is None: return None
		invalid_content_regexp = re.compile(r'''[`~!@#$%^&*()\-_=+[\]{};':"\\\|,\./<>?]|\s''')
		if invalid_content_regexp.search(text):
			return False
		if text in [text.lower(), text != text.upper()]:
			return False
		return True

	def remove_accent(self, text=None):
		return unidecode.unidecode(text)

	def clean_snake_case(self, text=None):
		snake_clean = re.sub('_+', '_', self.remove_accent(text))
		return snake_clean

	def text_to_alpha_numeric(self, text=None, replace_string=None):
		if replace_string is None: replace_string = '_'
		alphanumeric = re.sub('[^a-zA-Z0-9]+', replace_string, self.remove_accent(text))
		return alphanumeric

	def text_to_camel_case(self, text=None, case=None):
		if case is None: case = 'lower'
		camel_case = self.remove_accent(text).title().replace('_', '')
		camel_case = re.sub(r'[^a-zA-Z0-9]+', '', camel_case)
		camel_case = camel_case.replace(' ', '')
		if case.lower() == 'lower':
			camel_case = camel_case[0].lower() + camel_case[1:]
		return camel_case

	def camel_case_to_snake_case(self, text=None, case=None):
		if case is None: case = 'lower'
		first_cap_regexp = re.compile('(.)([A-Z][a-z]+)')
		all_cap_regexp = re.compile('([a-z0-9])([A-Z0-9])')

		snake_temp = first_cap_regexp.sub(r'\1_\2', self.remove_accent(text))
		snake = all_cap_regexp.sub(r'\1_\2', snake_temp).lower()
		snake_clean = self.clean_snake_case(snake)
		if case.lower() == 'upper':
			snake_clean = snake_clean.upper()
		return snake_clean

	def text_to_snake_case(self, text=None, case=None):
		if self.is_camel_case(text=text):
			return self.camel_case_to_snake_case(text=text, case=case)
		else:
			return self.camel_case_to_snake_case(self.text_to_camel_case(text=text), case=case)
