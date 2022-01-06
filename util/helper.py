import pandas as pd
import numpy as np 
import os
import datetime
import requests

util_dir = os.path.dirname(__file__)
data_dir = os.path.join(os.path.join(util_dir, os.pardir), 'data/')
vaccinations_filename = 'germany_vaccinations_timeseries_v2.tsv'

cases_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Altersverteilung.xlsx?__blob=publicationFile'
hospitalizations_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Klinische_Aspekte.xlsx?__blob=publicationFile'
deaths_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Projekte_RKI/COVID-19_Todesfaelle.xlsx?__blob=publicationFile'
amount_tests_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Testzahlen-gesamt.xlsx?__blob=publicationFile'
vaccinations_url = 'https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv'


def date_col(df, year_col='Meldejahr', week_col='Meldewoche'):
	"""Creates the column 'Meldedatum' in the dataframe for uniform indexing of dataframes

	Keyword arguments:
	df -- DataFrame for which the column should be created
	year_col -- The name of the column in df that contains the year
	week_col -- The name of the column in df that contains the week number (1-52)
	"""
	df[year_col] = df[year_col].astype(str)
	df[week_col] = df[week_col].astype(str)
	#df['Meldedatum'] = df[year_col] + '-' + df[week_col]
	df['Meldedatum'] = pd.to_datetime(df[week_col] + df[year_col].add('-1'), format='%V%G-%u')
	df.drop(columns=[year_col, week_col], inplace=True)
	return df

def date_to_week(df, date_col='date'):
	df['Meldejahr'] = pd.to_datetime(df[date_col], errors='coerce').dt.isocalendar().year
	df['Meldewoche'] = pd.to_datetime(df[date_col], errors='coerce').dt.isocalendar().week
	return df

def style_fig(fig, colors):
	fig.update_layout(
		plot_bgcolor=colors['tile'],
		paper_bgcolor=colors['background'],
		font_color=colors['text']
	)
	return fig

def collect_data():
	populations				= pd.read_csv(data_dir + 'population.csv')

	# cases
	r = requests.get(cases_url, allow_redirects=True)
	open(data_dir + 'cases.xlsx', 'wb').write(r.content)
	cases			= pd.read_excel(data_dir + 'cases.xlsx', sheet_name=1, header=0, index_col='Altersgruppe', engine='openpyxl')
	cases_incidence	= pd.read_excel(data_dir + 'cases.xlsx', sheet_name=0, header=0, index_col='Altersgruppe', engine='openpyxl')
	os.remove(data_dir + 'cases.xlsx')

	# transpose cases DataFrames
	cases = cases.T.reset_index()
	cases_incidence = cases_incidence.T.reset_index()

	cases.rename(columns=lambda x: x.strip(), inplace=True)
	cases_incidence.rename(columns=lambda x: x.strip(), inplace=True)

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

	cases[['Meldejahr', 'Meldewoche']]				= cases['index'].str.split('_', expand=True)
	cases_incidence[['Meldejahr', 'Meldewoche']]	= cases_incidence['index'].str.split('_', expand=True)

	cases					= date_col(cases)
	cases_incidence			= date_col(cases_incidence)

	cases.drop(columns=[
		'index', '0 - 4', '5 - 9', '10 - 14', '15 - 19', '20 - 24', '25 - 29', 
		'30 - 34', '35 - 39', '40 - 44', '45 - 49', '50 - 54', '55 - 59', 
		'60 - 64', '65 - 69', '70 - 74', '75 - 79', '80 - 84', '85 - 89', '90+'
		], inplace=True)
	cases_incidence.drop(columns=[
		'index', '0 - 4', '5 - 9', '10 - 14', '15 - 19', '20 - 24', 
		'25 - 29', '30 - 34', '35 - 39', '40 - 44', '45 - 49', '50 - 54', '55 - 59', 
		'60 - 64', '65 - 69', '70 - 74', '75 - 79', '80 - 84', '85 - 89', '90+'
		], inplace=True)

	cases.to_csv(data_dir + 'cases.csv', index=False)
	cases_incidence.to_csv(data_dir + 'cases_incidence.csv', index=False)


	# hospitalization
	r = requests.get(hospitalizations_url, allow_redirects=True)
	open(data_dir + 'hosp.xlsx', 'wb').write(r.content)
	hospitalizations_total	= pd.read_excel(data_dir + 'hosp.xlsx', sheet_name=0, header=3, engine='openpyxl')
	hospitalizations_age	= pd.read_excel(data_dir + 'hosp.xlsx', sheet_name=2, header=5, engine='openpyxl')
	os.remove(data_dir + 'hosp.xlsx')

	# interpolate missing values
	hospitalizations_age = hospitalizations_age.interpolate(method='linear')
	# add hospitalization incidence
	hospitalizations_age['Fälle Gesamt'] = hospitalizations_total['Anzahl hospitalisiert']
	hospitalizations_age['Inzidenz A00..04'] = (hospitalizations_age['Fälle A00..04'] / populations.at[0,'A00..04']) * 100000.0
	hospitalizations_age['Inzidenz A05..14'] = (hospitalizations_age['Fälle A05..14'] / populations.at[0,'A05..14']) * 100000.0
	hospitalizations_age['Inzidenz A15..34'] = (hospitalizations_age['Fälle A15..34'] / populations.at[0,'A15..34']) * 100000.0
	hospitalizations_age['Inzidenz A35..59'] = (hospitalizations_age['Fälle A35..59'] / populations.at[0,'A35..59']) * 100000.0
	hospitalizations_age['Inzidenz A60..79'] = (hospitalizations_age['Fälle A60..79'] / populations.at[0,'A60..79']) * 100000.0
	hospitalizations_age['Inzidenz A80+'] = (hospitalizations_age['Fälle A80+'] / populations.at[0,'A80+']) * 100000.0
	hospitalizations_age['Inzidenz Gesamt'] = (hospitalizations_total['Anzahl hospitalisiert'] / populations.at[0, 'total']) * 100000.0

	hospitalizations_age	= date_col(hospitalizations_age)

	hospitalizations_age.to_csv(data_dir + 'hospitalizations.csv', index=False)


	# deaths
	r = requests.get(deaths_url, allow_redirects=True)
	open(data_dir + 'deaths.xlsx', 'wb').write(r.content)
	deaths_total 	= pd.read_excel(data_dir + 'deaths.xlsx', sheet_name=2, header=0, engine='openpyxl')
	deaths_age		= pd.read_excel(data_dir + 'deaths.xlsx', sheet_name=4, header=0, engine='openpyxl')
	os.remove(data_dir + 'deaths.xlsx')

	# interpolate missing values
	np.random.seed(0)
	deaths_total = deaths_total.where(deaths_total != '<4', int(np.random.normal(2,1))).astype(int)
	deaths_age = deaths_age.where(deaths_age != '<4', int(np.random.normal(2,1))).astype(int)
	# add deaths age groups and incidence
	deaths_age['Fälle A00..19'] = deaths_age['AG 0-9 Jahre'] + deaths_age['AG 10-19 Jahre']
	deaths_age['Fälle A20..59'] = deaths_age['AG 20-29 Jahre'] + deaths_age['AG 30-39 Jahre'] + deaths_age['AG 40-49 Jahre'] + deaths_age['AG 50-59 Jahre']
	deaths_age['Fälle A60..79'] = deaths_age['AG 60-69 Jahre'] + deaths_age['AG 70-79 Jahre']
	deaths_age['Fälle A80+'] = deaths_age['AG 80-89 Jahre'] + deaths_age['AG 90+ Jahre']
	deaths_age['Fälle Gesamt'] = deaths_total['Anzahl verstorbene COVID-19 Fälle']
	deaths_age['Inzidenz A00..19'] = (deaths_age['Fälle A00..19'] / populations.at[0,'A00..19']) * 100000.0
	deaths_age['Inzidenz A20..59'] = (deaths_age['Fälle A20..59'] / populations.at[0,'A20..59']) * 100000.0
	deaths_age['Inzidenz A60..79'] = (deaths_age['Fälle A60..79'] / populations.at[0,'A60..79']) * 100000.0
	deaths_age['Inzidenz A80+'] = (deaths_age['Fälle A80+'] / populations.at[0,'A80+']) * 100000.0
	deaths_age['Inzidenz Gesamt'] = (deaths_total['Anzahl verstorbene COVID-19 Fälle'] / populations.at[0, 'total']) * 100000.0

	deaths_age				= date_col(deaths_age, year_col='Sterbejahr', week_col='Sterbewoche')

	deaths_age.drop(columns=[
		'AG 0-9 Jahre','AG 10-19 Jahre','AG 20-29 Jahre','AG 30-39 Jahre','AG 40-49 Jahre',
		'AG 50-59 Jahre','AG 60-69 Jahre','AG 70-79 Jahre','AG 80-89 Jahre','AG 90+ Jahre',
		], inplace=True)

	deaths_age.to_csv(data_dir + 'deaths.csv', index=False)

	
	# amount of tests
	r = requests.get(amount_tests_url, allow_redirects=True)
	open(data_dir + 'amount_tests.xlsx', 'wb').write(r.content)
	amount_tests = pd.read_excel(data_dir + 'amount_tests.xlsx', sheet_name=1, header=0, engine='openpyxl')
	os.remove(data_dir + 'amount_tests.xlsx')

	# clean up amount_test DataFrame
	amount_tests.at[0, 'Kalenderwoche'] = '10/2020'
	amount_tests = amount_tests[:-1] # delete last row since its just the total
	amount_tests['Positivenanteil (%)'] = (amount_tests['Positiv getestet'] / amount_tests['Anzahl Testungen']) * 100.0

	amount_tests[['Meldewoche', 'Meldejahr']]		= amount_tests['Kalenderwoche'].str.split('/', expand=True)

	amount_tests			= date_col(amount_tests)

	amount_tests.drop(columns=['Kalenderwoche'], inplace=True)
	amount_tests.to_csv(data_dir + 'amount_tests.csv', index=False)


	# vaccinations
	r = requests.get(vaccinations_url, allow_redirects=True)
	open(data_dir + 'vaccinations.tsv', 'wb').write(r.content)
	vaccinations			= pd.read_csv(data_dir + 'vaccinations.tsv', sep='\t', header=0)
	os.remove(data_dir + 'vaccinations.tsv')

	# add 'fully vaccinated' and 'boostered' column into vaccination DataFrame
	vaccinations['fully vaccinated'] = ((
		vaccinations['dosen_biontech_zweit_kumulativ'] + 
		vaccinations['dosen_moderna_zweit_kumulativ'] + 
		vaccinations['dosen_astra_zweit_kumulativ'] + 
		vaccinations['dosen_johnson_erst_kumulativ']
	) / populations.at[0, 'total']) * 100.0
	vaccinations['boostered'] = ((
		vaccinations['dosen_biontech_dritt_kumulativ'] +
		vaccinations['dosen_moderna_dritt_kumulativ'] + 
		vaccinations['dosen_astra_dritt_kumulativ'] + 
		vaccinations['dosen_johnson_zweit_kumulativ'] + 
		vaccinations['dosen_johnson_dritt_kumulativ']
	) / populations.at[0, 'total']) * 100.0
	# adjust vaccination DataFrame to have week column
	vaccinations = date_to_week(vaccinations)
	vaccinations = vaccinations.groupby(['Meldejahr', 'Meldewoche']).max().reset_index()

	# create column for calendar week
	vaccinations = date_col(vaccinations)

	vaccinations.drop(columns=[
		'date','dosen_kumulativ','dosen_erst_kumulativ','dosen_zweit_kumulativ','dosen_dritt_kumulativ',
		'dosen_biontech_kumulativ','dosen_biontech_erst_kumulativ','dosen_biontech_zweit_kumulativ','dosen_biontech_dritt_kumulativ',
		'dosen_moderna_kumulativ','dosen_moderna_erst_kumulativ','dosen_moderna_zweit_kumulativ','dosen_moderna_dritt_kumulativ',
		'dosen_astra_kumulativ','dosen_astra_erst_kumulativ','dosen_astra_zweit_kumulativ','dosen_astra_dritt_kumulativ',
		'dosen_johnson_kumulativ','dosen_johnson_erst_kumulativ','dosen_johnson_zweit_kumulativ','dosen_johnson_dritt_kumulativ',
		'dosen_differenz_zum_vortag','dosen_erst_differenz_zum_vortag','dosen_zweit_differenz_zum_vortag','dosen_dritt_differenz_zum_vortag',
		'dosen_vollstaendig_differenz_zum_vortag','personen_erst_kumulativ','personen_voll_kumulativ','personen_auffrisch_kumulativ',
		'impf_quote_erst','impf_quote_voll','dosen_dim_kumulativ','dosen_kbv_kumulativ','indikation_alter_dosen','indikation_beruf_dosen',
		'indikation_medizinisch_dosen','indikation_pflegeheim_dosen','indikation_alter_erst','indikation_beruf_erst','indikation_medizinisch_erst',
		'indikation_pflegeheim_erst','indikation_alter_voll','indikation_beruf_voll','indikation_medizinisch_voll','indikation_pflegeheim_voll',
		], inplace=True)

	vaccinations.to_csv(data_dir + 'vaccinations.csv', index=False)