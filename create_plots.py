# pandas for data processing
import pandas as pd
import numpy as np
import os

# import other files for plotting
from cases import plot_cases, plot_cases_by_age, plot_cases_positivityrate
from deaths import plot_deaths, plot_deaths_by_age
from hospitalizations import plot_hospitalizations, plot_hospitalizations_by_age
from vaccine_effectiveness import plot_hospitalization_rate
from util.helper import collect_data, date_col, date_to_week

# files and directories
data_dir = os.path.join(os.path.dirname(__file__), 'data/')
cases_filename = 'Altersverteilung.xlsx'
clinical_filename = 'Klinische_Aspekte.xlsx'
deaths_filename = 'COVID-19_Todesfaelle.xlsx'
amount_tests_filename = 'Testzahlen-gesamt.xlsx'
vaccinations_filename = 'germany_vaccinations_timeseries_v2.tsv'
populations_filename = 'Bevoelkerung_Altersgruppen.csv'

# figure dictionary
figs = {}

def create_plots():
	# ------------------------------
	# ------- PREPROCESSING --------
	# ------------------------------
	collect_data()

	# get DataFrames from excel files
	# population by age(groups)
	populations				= pd.read_csv(data_dir + populations_filename, sep=';', header=0, index_col='Alter', encoding='latin-1')
	# cases
	cases					= pd.read_excel(data_dir + cases_filename, sheet_name=0, header=0, index_col='Altersgruppe', engine='openpyxl')
	cases_incidence			= pd.read_excel(data_dir + cases_filename, sheet_name=1, header=0, index_col='Altersgruppe', engine='openpyxl')
	# hospitalizations
	hospitalizations_total	= pd.read_excel(data_dir + clinical_filename, sheet_name=0, header=3, engine='openpyxl')
	hospitalizations_age	= pd.read_excel(data_dir + clinical_filename, sheet_name=2, header=5, engine='openpyxl')
	# deaths
	deaths_total 			= pd.read_excel(data_dir + deaths_filename, sheet_name=2, header=0, engine='openpyxl')
	deaths_age				= pd.read_excel(data_dir + deaths_filename, sheet_name=4, header=0, engine='openpyxl')
	# amount of tests
	amount_tests			= pd.read_excel(data_dir + amount_tests_filename, sheet_name=1, header=0, engine='openpyxl')
	# vaccinations
	vaccinations			= pd.read_csv(data_dir + vaccinations_filename, sep='\t', header=0)

	# DataFrame-/file-specific preprocessing
	# consistent age groups in population DataFrame
	total_population = populations['31.12.2020'].sum()
	populations = populations.T.reset_index()
	populations['A00..04'] = populations['unter 1 Jahr']
	populations['A00..04'] += sum([populations[f'{i}-Jährige'] for i in range(1,5)])
	populations['A05..14'] = sum([populations[f'{i}-Jährige'] for i in range(5,15)])
	populations['A15..34'] = sum([populations[f'{i}-Jährige'] for i in range(15,35)])
	populations['A35..59'] = sum([populations[f'{i}-Jährige'] for i in range(35,60)])
	populations['A60..79'] = sum([populations[f'{i}-Jährige'] for i in range(60,80)])

	populations['A00..19'] = populations['unter 1 Jahr']
	populations['A00..19'] += sum([populations[f'{i}-Jährige'] for i in range(1,20)])
	populations['A20..59'] = sum([populations[f'{i}-Jährige'] for i in range(20, 60)])

	populations['A80+'] = sum([populations[f'{i}-Jährige'] for i in range(80,85)])
	populations['A80+'] += populations['85 Jahre und mehr']

	# interpolate missing values
	hospitalizations_age = hospitalizations_age.interpolate(method='linear')
	np.random.seed(0)
	deaths_total = deaths_total.where(deaths_total != '<4', int(np.random.normal(2,1))).astype(int)
	deaths_age = deaths_age.where(deaths_age != '<4', int(np.random.normal(2,1))).astype(int)
	# add hospitalization incidence
	hospitalizations_total['Inzidenz'] = (hospitalizations_total['Anzahl hospitalisiert'] / total_population) * 100000.0
	hospitalizations_age['Inzidenz A00..04'] = (hospitalizations_age['Fälle A00..04'] / populations.at[0,'A00..04']) * 100000.0
	hospitalizations_age['Inzidenz A05..14'] = (hospitalizations_age['Fälle A05..14'] / populations.at[0,'A05..14']) * 100000.0
	hospitalizations_age['Inzidenz A15..34'] = (hospitalizations_age['Fälle A15..34'] / populations.at[0,'A15..34']) * 100000.0
	hospitalizations_age['Inzidenz A35..59'] = (hospitalizations_age['Fälle A35..59'] / populations.at[0,'A35..59']) * 100000.0
	hospitalizations_age['Inzidenz A60..79'] = (hospitalizations_age['Fälle A60..79'] / populations.at[0,'A60..79']) * 100000.0
	hospitalizations_age['Inzidenz A80+'] = (hospitalizations_age['Fälle A80+'] / populations.at[0,'A80+']) * 100000.0
	# add deaths age groups and incidence
	deaths_total['Inzidenz'] = (deaths_total['Anzahl verstorbene COVID-19 Fälle'] / total_population) * 100000.0
	deaths_age['Fälle A00..19'] = deaths_age['AG 0-9 Jahre'] + deaths_age['AG 10-19 Jahre']
	deaths_age['Fälle A20..59'] = deaths_age['AG 20-29 Jahre'] + deaths_age['AG 30-39 Jahre'] + deaths_age['AG 40-49 Jahre'] + deaths_age['AG 50-59 Jahre']
	deaths_age['Fälle A60..79'] = deaths_age['AG 60-69 Jahre'] + deaths_age['AG 70-79 Jahre']
	deaths_age['Fälle A80+'] = deaths_age['AG 80-89 Jahre'] + deaths_age['AG 90+ Jahre']
	deaths_age['Inzidenz A00..19'] = (deaths_age['Fälle A00..19'] / populations.at[0,'A00..19']) * 100000.0
	deaths_age['Inzidenz A20..59'] = (deaths_age['Fälle A20..59'] / populations.at[0,'A20..59']) * 100000.0
	deaths_age['Inzidenz A60..79'] = (deaths_age['Fälle A60..79'] / populations.at[0,'A60..79']) * 100000.0
	deaths_age['Inzidenz A80+'] = (deaths_age['Fälle A80+'] / populations.at[0,'A80+']) * 100000.0
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
	cases_incidence['Inzidenz A00..04'] = (cases['Fälle A00..04'] / populations.at[0,'A00..04']) * 100000.0
	cases_incidence['Inzidenz A05..14'] = (cases['Fälle A05..14'] / populations.at[0,'A05..14']) * 100000.0
	cases_incidence['Inzidenz A15..34'] = (cases['Fälle A15..34'] / populations.at[0,'A15..34']) * 100000.0
	cases_incidence['Inzidenz A35..59'] = (cases['Fälle A35..59'] / populations.at[0,'A35..59']) * 100000.0
	cases_incidence['Inzidenz A60..79'] = (cases['Fälle A60..79'] / populations.at[0,'A60..79']) * 100000.0
	cases_incidence['Inzidenz A80+'] = (cases['Fälle A80+'] / populations.at[0,'A80+']) * 100000.0
	# clean up amount_test DataFrame
	amount_tests.at[0, 'Kalenderwoche'] = '10/2020'
	amount_tests = amount_tests[:-1] # delete last row since its just the total
	amount_tests['Positivenanteil (%)'] = (amount_tests['Positiv getestet'] / amount_tests['Anzahl Testungen']) * 100.0
	# add 'fully vaccinated' and 'boostered' column into vaccination DataFrame
	vaccinations['fully vaccinated'] = ((
		vaccinations['dosen_biontech_zweit_kumulativ'] + 
		vaccinations['dosen_moderna_zweit_kumulativ'] + 
		vaccinations['dosen_astra_zweit_kumulativ'] + 
		vaccinations['dosen_johnson_erst_kumulativ']
	) / total_population) * 100.0
	vaccinations['boostered'] = ((
		vaccinations['dosen_biontech_dritt_kumulativ'] +
		vaccinations['dosen_moderna_dritt_kumulativ'] + 
		vaccinations['dosen_astra_dritt_kumulativ'] + 
		vaccinations['dosen_johnson_zweit_kumulativ'] + 
		vaccinations['dosen_johnson_dritt_kumulativ']
	) / total_population) * 100.0
	# adjust vaccination DataFrame to have week column
	vaccinations = date_to_week(vaccinations)
	vaccinations = vaccinations.groupby(['Meldejahr', 'Meldewoche']).max().reset_index()

	# create new columns for better processing
	cases[['Meldejahr', 'Meldewoche']]				= cases['index'].str.split('_', expand=True)
	cases_incidence[['Meldejahr', 'Meldewoche']]	= cases_incidence['index'].str.split('_', expand=True)
	amount_tests[['Meldewoche', 'Meldejahr']]		= amount_tests['Kalenderwoche'].str.split('/', expand=True)

	# create column for calendar week
	hospitalizations_total	= date_col(hospitalizations_total, week_col='MW')
	hospitalizations_age	= date_col(hospitalizations_age)
	cases					= date_col(cases)
	cases_incidence			= date_col(cases_incidence)
	deaths_total			= date_col(deaths_total, year_col='Sterbejahr', week_col='Sterbewoche')
	deaths_age				= date_col(deaths_age, year_col='Sterbejahr', week_col='Sterbewoche')
	amount_tests			= date_col(amount_tests)
	vaccinations			= date_col(vaccinations)

	# ------------------------------
	# --------- PLOT DATA ----------
	# ------------------------------
	# create plots
	figs['cases-total'], figs['cases-incidence-total']		= plot_cases(cases, cases_incidence)
	figs['cases-by-age'], figs['cases-incidence-by-age']	= plot_cases_by_age(cases, cases_incidence)
	figs['hosp-total'], figs['hosp-incidence-total']		= plot_hospitalizations(hospitalizations_total)
	figs['hosp-by-age'], figs['hosp-incidence-by-age']		= plot_hospitalizations_by_age(hospitalizations_age)
	figs['deaths-total'], figs['deaths-incidence-total']	= plot_deaths(deaths_total)
	figs['deaths-by-age'], figs['deaths-incidence-by-age']	= plot_deaths_by_age(deaths_age)
	figs['test-positivity-rate']							= plot_cases_positivityrate(cases, amount_tests)
	figs['hosp-rate']										= plot_hospitalization_rate(hospitalizations_total, cases, vaccinations)

	return figs