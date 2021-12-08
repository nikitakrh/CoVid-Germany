import pandas as pd
import os

from hospitalizations import plot_hospitalizations
from cases import plot_cases_by_age, plot_cases_positivityrate
from vaccine_effectiveness import plot_hospitalization_rate
from util.helper import date_col, date_to_week


data_dir = os.path.join(os.path.dirname(__file__), 'data/')
clinical_filename = 'Klinische_Aspekte.xlsx'
cases_filename = 'Altersverteilung.xlsx'
amount_tests_filename = 'Testzahlen-gesamt.xlsx'
vaccinations_filename = 'germany_vaccinations_timeseries_v2.tsv'

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
	hospitalizations_total = pd.read_excel(data_dir + clinical_filename, sheet_name=0, header=3, engine='openpyxl')
	hospitalizations_age = pd.read_excel(data_dir + clinical_filename, sheet_name=2, header=5, engine='openpyxl')
	hospitalizations_age_incidence = pd.read_excel(data_dir + clinical_filename, sheet_name=4, header=4, engine='openpyxl')
	# cases
	cases = pd.read_excel(data_dir + cases_filename, sheet_name=0, header=0, index_col='Altersgruppe', engine='openpyxl')
	cases_incidence = pd.read_excel(data_dir + cases_filename, sheet_name=1, header=0, index_col='Altersgruppe', engine='openpyxl')
	# amount of tests
	amount_tests = pd.read_excel(data_dir + amount_tests_filename, sheet_name=1, header=0, engine='openpyxl')
	# vaccinations
	vaccinations = pd.read_csv(data_dir + vaccinations_filename, sep='\t', header=0)

	# DataFrame-/file-specific preprocessing
	# interpolate missing values
	hospitalizations_age = hospitalizations_age.interpolate(method='linear')
	# transpose cases DataFrames
	cases = cases.T.reset_index()
	cases_incidence = cases_incidence.T.reset_index()
	# generate new age groups
	cases['Fälle A00..04'] = cases['0 - 4']
	cases['Fälle A05..14'] = cases['5 - 9'] + cases['10 - 14']
	cases['Fälle A15..34'] = cases['15 - 19'] + cases['20 - 24'] + cases['25 - 29'] + cases['30 - 34']
	cases['Fälle A35..59'] = cases['35 - 39'] + cases['40 - 44'] + cases['45 - 49'] + cases['50 - 54'] + cases['55 - 59']
	cases['Fälle A60..79'] = cases['60 - 64'] + cases['65 - 69'] + cases['70 - 74'] + cases['75 - 79']
	cases['Fälle A80+'] = cases['80 - 84'] + cases['85 - 89'] + cases['90+']
	# clean up amount_test DataFrame
	amount_tests.at[0, 'Kalenderwoche'] = '10/2020'
	amount_tests = amount_tests[:-1] # delete last row since its just the total
	amount_tests['Positivenanteil (%)'] = (amount_tests['Positiv getestet'] / amount_tests['Anzahl Testungen']) * 100.0
	# adjust vaccination DataFrame to have week column
	vaccinations = date_to_week(vaccinations)

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
	plot_cases_positivityrate(cases, amount_tests)
	plot_hospitalization_rate(hospitalizations_total, cases)

if __name__ == '__main__':
	main()