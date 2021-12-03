import pandas as pd
import os

from hospitalizations import plot_hospitalizations
from cases import plot_cases_by_age, plot_cases_total
from util.helper import date_col


data_dir = os.path.join(os.path.dirname(__file__), 'data/')
clinical_filename = 'Klinische_Aspekte.xlsx'
cases_filename = 'Altersverteilung.xlsx'
amount_tests_filename = 'Testzahlen-gesamt.xlsx'

def collect_data():
	# TODO: download data automatically
	pass

def main():
	# ------------------------------
	# ------- PREPROCESSING --------
	# ------------------------------
	collect_data()

	# get DataFrames from excel files
	# hospitalizations
	hospitalizations_total = pd.read_excel(data_dir + clinical_filename, sheet_name=0, header=3)
	hospitalizations_age = pd.read_excel(data_dir + clinical_filename, sheet_name=2, header=5)
	hospitalizations_age_incidence = pd.read_excel(data_dir + clinical_filename, sheet_name=4, header=4)
	# cases
	cases = pd.read_excel(data_dir + cases_filename, sheet_name=0, header=0, index_col='Altersgruppe')
	cases_incidence = pd.read_excel(data_dir + cases_filename, sheet_name=1, header=0, index_col='Altersgruppe')
	# amount of tests
	amount_tests = pd.read_excel(data_dir + amount_tests_filename, sheet_name=1, header=0)

	# DataFrame-/file-specific preprocessing
	# transpose cases DataFrames
	cases = cases.T.reset_index()
	cases_incidence = cases_incidence.T.reset_index()
	# clean up amount_test DataFrame
	amount_tests.at[0, 'Kalenderwoche'] = '10/2020'
	amount_tests = amount_tests[:-1] # delete last row since its just the total
	amount_tests['Positivenanteil (%)'] = (amount_tests['Positiv getestet'] / amount_tests['Anzahl Testungen']) * 100.0

	# create new columns for better processing
	cases[['Meldejahr', 'Meldewoche']] = cases['index'].str.split('_', expand=True)
	cases_incidence[['Meldejahr', 'Meldewoche']] = cases_incidence['index'].str.split('_', expand=True)
	amount_tests[['Meldewoche', 'Meldejahr']] = amount_tests['Kalenderwoche'].str.split('/', expand=True)

	# create column for calendar week
	hospitalizations_total = date_col(hospitalizations_total, week_col='MW')
	hospitalizations_age = date_col(hospitalizations_age)
	hospitalizations_age_incidence = date_col(hospitalizations_age_incidence)
	cases = date_col(cases)
	cases_incidence = date_col(cases_incidence)
	amount_tests = date_col(amount_tests)


	# ------------------------------
	# --------- PLOT DATA ----------
	# ------------------------------

	# create plots
	plot_hospitalizations(hospitalizations_total, hospitalizations_age, hospitalizations_age_incidence)
	plot_cases_by_age(cases, cases_incidence)
	plot_cases_total(cases, amount_tests)

if __name__ == '__main__':
	main()