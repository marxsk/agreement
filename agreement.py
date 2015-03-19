#!/usr/bin/python -tt

""" Agreement module is counting inter-annotator agreement
	Currently, only Cohen's kappa between N raters is supported.
"""

import numpy as np

def cohen_kappa(original_data):
	""" Count Cohen's kappa for two annotators and N-class ratings

	    Data are expect to be np.array with two columns (one per annotator)
	    load data using: np.loadtxt(filename, delimiter=",", dtype="unicode")
	"""
	original_categories = np.unique(original_data.flatten())
	original_categories.sort()
	data = np.array(original_data, copy=True)

	trans_dict = {}
	freq_table = None

	def _replace_string_with_int():
		""" Loaded data have unicode values but we need them as int

		    numpy works best with normal array where indexes are int.
		    Input data are unicode strings like "***" or "yes". Translation
		    dictionary is created and then used for changing all values in array.
		    In case of need it can be also used to re-create original data.
		"""
		for i in xrange(original_categories.shape[0]):
			trans_dict[original_categories[i]] = i

		for rating in np.nditer(data, op_flags=['readwrite']):
			rating[...] = trans_dict[rating.item()]
		return data.astype(np.int64, copy=False)

	def _set_frequency_table():
		""" Prepare frequency table of unique ratings """
		def put_rating(ratings):
			""" Value of rating increases an appropriate field in frequency table """
			freq_table[ratings[0]][ratings[1]] += 1
			return 0

		freq_table = np.zeros((original_categories.shape[0], original_categories.shape[0]))
		np.apply_along_axis(put_rating, 1, data)
		return freq_table

	def _probability_observed():
		""" Count observed probability of agreement = pr(A) in Cohen's equation """
		return 1.0 * np.sum(np.diag(freq_table)) / np.sum(freq_table)

	def _probability_expected():
		""" Count expected probability of random agreement = pr(E) in Cohen's equation """
		pr_expected = 0
		for i in xrange(original_categories.shape[0]):
			pr_expected += np.sum(freq_table[i, :]) * np.sum(freq_table[:, i])
		return 1.0 * pr_expected / (np.sum(freq_table) ** 2)

	data = _replace_string_with_int()
	freq_table = _set_frequency_table()
	return 1.0 * (_probability_observed() - _probability_expected()) / (1.0 - _probability_expected())

def load_data(filename):
	""" Load CSV-style data exported from OpenOffice Calc/MS Office

	    This version do not count with headers yet.
	"""
	return np.loadtxt(filename, delimiter=",", dtype="unicode")
