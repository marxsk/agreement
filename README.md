# agreement
Library for measuring inter/intra annotator agreement

Usage:

Let's assume that we have CVS file with two columns (one per rater) and one line per each rated item.

data = np.loadtxt(csv_filename, delimiter=",", dtype="unicode")
print agreement.cohen_kappa(data)

This is library in development which was motivated by need for counting Cohen's kappa (and possibly other measures too) and I wanted to try to use numpy for something else than examples on Coursera.
