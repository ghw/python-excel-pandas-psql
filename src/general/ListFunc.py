class ListFunc(object):

	def __init__(self):
		pass

	def get_unique_list(self, list_with_duplicates=None, sorted=None, reversed=None):
		if sorted is None:
			sorted = False
		if reversed is None:
			reversed = False

		unique_list = list(set(list_with_duplicates))
		if sorted:
			unique_list.sort(reverse=reversed)

		return unique_list

	def get_common_items(self, list_one=None, list_two=None):
		return list(set(list_one).intersection(list_two))

	def get_all_items(self, list_one=None, list_two=None):
		return list(set(list_one).union(list_two))

	def get_flat_list(self, list_of_lists=None):
		flat_list = [item for sub_list in list_of_lists for item in sub_list]
		return flat_list
