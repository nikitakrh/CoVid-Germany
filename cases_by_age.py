import pandas as pd 
import numpy as np
import os
import matplotlib.pyplot as plt

data_dir = os.path.join(os.path.dirname(__file__), 'data/')
cases_filename = 'Altersverteilung.xlsx'

# TODO: plot cases and hospitalizations by age for each agegroup
# TODO: plot cases as positive test rate

def main():
	cases_age = pd.read_excel(data_dir + cases_filename, sheet_name=0, header=0, index_col='Altersgruppe')
	cases_age_incidence = pd.read_excel(data_dir + cases_filename, sheet_name=1, header=0, index_col='Altersgruppe')

	# Transpose dataframe
	cases_age = cases_age.T
	cases_age_incidence = cases_age_incidence.T

	# Create plot for hospitalizations (total and rate)
	fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

	ax1.set_title('Cases of CoViD-19 in Germany')
	ax1.set_ylabel('Case')

	# TODO: get age groups programmatically

	ax1.plot(cases_age.index, cases_age['Gesamt'], label='Total')
	ax1.plot(cases_age.index, cases_age['90+'], label='90+')
	for i in range(85, 0, -5):
		agegroup = str(i) + ' - ' + str(i+4)
		ax1.plot(cases_age.index, cases_age[agegroup], label=agegroup)

	ax1.legend()

	ax2.set_ylabel('Case Incidence by Age')
	ax2.set_xlabel('Year-Calendar Week')

	ax2.plot(cases_age_incidence.index, cases_age_incidence['Gesamt'], label='Total')
	ax2.plot(cases_age_incidence.index, cases_age_incidence['90+'], label='90+')
	for i in range(85, 0, -5):
		agegroup = str(i) + ' - ' + str(i+4)
		ax2.plot(cases_age_incidence.index, cases_age_incidence[agegroup], label=agegroup)

	ax2.legend()

	plt.xticks(rotation=45)
	n = 2  # Keeps every 2nd label
	[l.set_visible(False) for (i,l) in enumerate(ax1.xaxis.get_ticklabels()) if i % n != 0]

	plt.show()


if __name__ == '__main__':
	main()