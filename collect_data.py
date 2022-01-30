import os
import requests
import pandas as pd 
import numpy as np
from datetime import datetime, timedelta

from util.helper import download_data

data_dir = os.path.join(os.path.dirname(__file__), 'data/')

daily_cases_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Fallzahlen_Gesamtuebersicht.xlsx?__blob=publicationFile'
cases_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Altersverteilung.xlsx?__blob=publicationFile'
hospitalizations_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Klinische_Aspekte.xlsx?__blob=publicationFile'
deaths_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Projekte_RKI/COVID-19_Todesfaelle.xlsx?__blob=publicationFile'
amount_tests_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Testzahlen-gesamt.xlsx?__blob=publicationFile'
vaccinations_url = 'https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv'

vaxx_rate_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx?__blob=publicationFile'
cases_by_state_url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Fallzahlen_Inzidenz_aktualisiert.xlsx?__blob=publicationFile'

populations = None
days_to_predict = 30



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

def predict_cases(daily_cases):
	# import here to speed up other figures
	from sklearn.preprocessing import MinMaxScaler

	# window size for training
	days = 90

	array = []
	array_temp = []
	train_data = []
	train_labels = []

	for i in range(len(daily_cases)):
		array_temp.append(daily_cases.at[i, 'avg_cases'])
	array_temp = np.array(array_temp).reshape(-1,1)

	scaler = MinMaxScaler()
	array_temp = scaler.fit_transform(array_temp)
	array_temp = array_temp.tolist()
	for i in array_temp:
		array.append(i[0])
	k = 0
	for i in range(len(array)):
		try:
			train_data.append(array[k:days + k]) # Creating inner lists with 'days' days of data
			train_labels.append([array[days + k]])
			k += 1
		except:
			break
	length = max(map(len, train_data))
	train_data = np.array([xi + [None] * (length - len(xi)) for xi in train_data]).astype('float32')
	length = max(map(len, train_labels))
	train_labels = np.array([xi + [None] * (length - len(xi)) for xi in train_labels]).astype('float32')

	train_data = train_data[:len(train_labels)]
	train_data = np.expand_dims(train_data, 1)

	# build LSTM model for prediction
	# https://www.sciencedirect.com/science/article/pii/S0925231221015150#f0005
	from tensorflow import keras
	from tensorflow.keras.models import Sequential
	from tensorflow.keras.layers import LSTM, Activation, Dense, Dropout
	from tensorflow.keras.callbacks import EarlyStopping

	model = Sequential()
	model.add(LSTM(250, input_shape=(1, days), name='lstm1'))
	model.add(Dropout(0.5, name='dropout1'))
	model.add(Dense(250, activation='relu', name='fc2'))
	model.add(Dropout(0.5, name='dropout2'))
	model.add(Dense(days, activation='relu', name='fc3'))
	model.add(Dropout(0.5, name='dropout3'))
	model.add(Dense(1, activation='relu', name='fc4'))

	model.compile(loss='mean_squared_error', optimizer='adam')
	model.summary()

	epochs = 1000
	callback = EarlyStopping(monitor='loss', mode='min', patience=20)
	H = model.fit(train_data, train_labels, epochs=epochs, verbose=2, callbacks=[callback])

	# get predictions
	seed = array[-days:]
	for _ in range(days_to_predict):
		current_days = seed[-days:]
		current_days = np.squeeze(current_days)
		current_days = np.expand_dims(current_days, 0)
		current_days = np.expand_dims(current_days, 0)
		pred = model.predict(current_days)
		seed = np.append(seed, pred)

	# upcoming days prediction
	upcoming_days_prediction = scaler.inverse_transform(seed[-days_to_predict:].reshape(-1, 1))

	return upcoming_days_prediction

def collect_daily_cases():
	daily_cases = download_data(daily_cases_url, sheet=0, header=2)

	daily_cases['Date'] = pd.to_datetime(daily_cases['Berichtsdatum'], format='%Y-%m-%d')

	# check if already made predictions for the next 30 days
	if(os.path.exists(data_dir + 'daily_cases.csv')):
		last_date = daily_cases.iloc[-1]['Date'] + timedelta(days=days_to_predict)
		daily_cases_csv = pd.read_csv(data_dir + 'daily_cases.csv')
		last_date_predicted = datetime.strptime(daily_cases_csv.iloc[-1]['Date'], '%Y-%m-%d')
		if(last_date <= last_date_predicted):
			# already predicted
			return

	daily_cases.at[0, 'Differenz Vortag Fälle'] = daily_cases.at[0, 'Anzahl COVID-19-Fälle']
	daily_cases.drop(columns=[
		'Berichtsdatum', 'Anzahl COVID-19-Fälle', 'Todesfälle', 'Differenz Vortag Todesfälle', 'Fall-Verstorbenen-Anteil', 'Fälle ohne Todesfälle'
		], inplace=True)

	# make 7-day moving average for smoother plot and prediction
	daily_cases['avg_cases'] = daily_cases['Differenz Vortag Fälle'].rolling(window=7, min_periods=1).mean()

	# predict the cases for the next 30 days and store in array
	upcoming_days_prediction = predict_cases(daily_cases)

	# find the last date for which data exists
	last_date = daily_cases.iloc[-1]['Date']

	# make array with the next 30 days to append to dataframe
	upcoming_days = [last_date + timedelta(days=x+1) for x in range(days_to_predict)]
	upcoming_days = np.expand_dims(upcoming_days, axis=-1)

	upcoming_days_prediction = np.stack([upcoming_days, upcoming_days_prediction], axis=0)
	upcoming_days_prediction = np.reshape(upcoming_days_prediction, (2, days_to_predict)).transpose()

	pred_df = pd.DataFrame(upcoming_days_prediction, columns={'Date', 'avg_cases'})
	daily_cases = daily_cases.append(pred_df)

	daily_cases.to_csv(data_dir + 'daily_cases.csv', index=False)

def collect_cases():
	global populations

	# cases
	cases 			= download_data(cases_url, sheet=0, header=0, index_col='Altersgruppe')
	cases_incidence = download_data(cases_url, sheet=1, header=0, index_col='Altersgruppe')

	# transpose cases DataFrames
	cases 			= cases.T.reset_index()
	cases_incidence = cases_incidence.T.reset_index()

	cases.rename(columns=lambda x: x.strip(), inplace=True)
	cases_incidence.rename(columns=lambda x: x.strip(), inplace=True)

	# generate new age groups
	cases['Cases 0-4y'] = cases['0 - 4']
	cases['Cases 5-14y'] = cases['5 - 9'] + cases['10 - 14']
	cases['Cases 15-34y'] = cases['15 - 19'] + cases['20 - 24'] + cases['25 - 29'] + cases['30 - 34']
	cases['Cases 35-59y'] = cases['35 - 39'] + cases['40 - 44'] + cases['45 - 49'] + cases['50 - 54'] + cases['55 - 59']
	cases['Cases 60-79y'] = cases['60 - 64'] + cases['65 - 69'] + cases['70 - 74'] + cases['75 - 79']
	cases['Cases 80+y'] = cases['80 - 84'] + cases['85 - 89'] + cases['90+']
	cases_incidence['Incidence 0-4y'] = (cases['Cases 0-4y'] / populations.at[0,'0-4y']) * 100000.0
	cases_incidence['Incidence 5-14y'] = (cases['Cases 5-14y'] / populations.at[0,'5-14y']) * 100000.0
	cases_incidence['Incidence 15-34y'] = (cases['Cases 15-34y'] / populations.at[0,'15-34y']) * 100000.0
	cases_incidence['Incidence 35-59y'] = (cases['Cases 35-59y'] / populations.at[0,'35-59y']) * 100000.0
	cases_incidence['Incidence 60-79y'] = (cases['Cases 60-79y'] / populations.at[0,'60-79y']) * 100000.0
	cases_incidence['Incidence 80+y'] = (cases['Cases 80+y'] / populations.at[0,'80+y']) * 100000.0

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

def collect_hospitalizations():
	global populations

	# hospitalization
	hospitalizations_total = download_data(hospitalizations_url, sheet=0, header=3)
	hospitalizations_age   = download_data(hospitalizations_url, sheet=2, header=5)

	hospitalizations_age	= date_col(hospitalizations_age)
	hospitalizations_total	= date_col(hospitalizations_total, week_col='MW')
	hospitalizations_age = pd.merge(hospitalizations_age, hospitalizations_total[['Meldedatum', 'Anzahl hospitalisiert']], how='inner', on='Meldedatum')

	# rename columns
	hospitalizations_age.rename(columns={
			'Fälle A00..04': 'Cases 0-4y', 'Fälle A05..14': 'Cases 5-14y', 'Fälle A15..34': 'Cases 15-34y',
			'Fälle A35..59': 'Cases 35-59y', 'Fälle A60..79': 'Cases 60-79y', 'Fälle A80+': 'Cases 80+y',
			'Anzahl hospitalisiert': 'Total Cases'
			}, inplace=True)
	# add hospitalization incidence

	# interpolate missing values
	hospitalizations_age = hospitalizations_age.interpolate(method='linear')
	hospitalizations_age.fillna(0) # if impossible to interpolate, fill missing with 0

	hospitalizations_age['Incidence 0-4y'] = (hospitalizations_age['Cases 0-4y'] / populations.at[0,'0-4y']) * 100000.0
	hospitalizations_age['Incidence 5-14y'] = (hospitalizations_age['Cases 5-14y'] / populations.at[0,'5-14y']) * 100000.0
	hospitalizations_age['Incidence 15-34y'] = (hospitalizations_age['Cases 15-34y'] / populations.at[0,'15-34y']) * 100000.0
	hospitalizations_age['Incidence 35-59y'] = (hospitalizations_age['Cases 35-59y'] / populations.at[0,'35-59y']) * 100000.0
	hospitalizations_age['Incidence 60-79y'] = (hospitalizations_age['Cases 60-79y'] / populations.at[0,'60-79y']) * 100000.0
	hospitalizations_age['Incidence 80+y'] = (hospitalizations_age['Cases 80+y'] / populations.at[0,'80+y']) * 100000.0
	hospitalizations_age['Total Incidence'] = (hospitalizations_age['Total Cases'] / populations.at[0, 'total']) * 100000.0

	hospitalizations_age.to_csv(data_dir + 'hospitalizations.csv', index=False)

def collect_deaths():
	global populations

	# deaths
	deaths_total = download_data(deaths_url, sheet=2, header=0)
	deaths_age = download_data(deaths_url, sheet=4, header=0)

	# interpolate missing values
	np.random.seed(0)
	deaths_total = deaths_total.where(deaths_total != '<4', int(np.random.normal(2,1))).astype(int)
	deaths_age = deaths_age.where(deaths_age != '<4', int(np.random.normal(2,1))).astype(int)
	# add deaths age groups and incidence
	deaths_age['Cases 0-19y'] = deaths_age['AG 0-9 Jahre'] + deaths_age['AG 10-19 Jahre']
	deaths_age['Cases 20-59y'] = deaths_age['AG 20-29 Jahre'] + deaths_age['AG 30-39 Jahre'] + deaths_age['AG 40-49 Jahre'] + deaths_age['AG 50-59 Jahre']
	deaths_age['Cases 60-79y'] = deaths_age['AG 60-69 Jahre'] + deaths_age['AG 70-79 Jahre']
	deaths_age['Cases 80+y'] = deaths_age['AG 80-89 Jahre'] + deaths_age['AG 90+ Jahre']
	deaths_age['Total Cases'] = deaths_total['Anzahl verstorbene COVID-19 Fälle']
	deaths_age['Incidence 0-19y'] = (deaths_age['Cases 0-19y'] / populations.at[0,'0-19y']) * 100000.0
	deaths_age['Incidence 20-59y'] = (deaths_age['Cases 20-59y'] / populations.at[0,'20-59y']) * 100000.0
	deaths_age['Incidence 60-79y'] = (deaths_age['Cases 60-79y'] / populations.at[0,'60-79y']) * 100000.0
	deaths_age['Incidence 80+y'] = (deaths_age['Cases 80+y'] / populations.at[0,'80+y']) * 100000.0
	deaths_age['Total Incidence'] = (deaths_total['Anzahl verstorbene COVID-19 Fälle'] / populations.at[0, 'total']) * 100000.0

	deaths_age				= date_col(deaths_age, year_col='Sterbejahr', week_col='Sterbewoche')

	deaths_age.drop(columns=[
		'AG 0-9 Jahre','AG 10-19 Jahre','AG 20-29 Jahre','AG 30-39 Jahre','AG 40-49 Jahre',
		'AG 50-59 Jahre','AG 60-69 Jahre','AG 70-79 Jahre','AG 80-89 Jahre','AG 90+ Jahre',
		], inplace=True)

	deaths_age.to_csv(data_dir + 'deaths.csv', index=False)

def collect_tests():
	# amount of tests
	amount_tests = download_data(amount_tests_url, sheet=1, header=0)

	# clean up amount_test DataFrame
	amount_tests.at[0, 'Kalenderwoche'] = '10/2020'
	amount_tests = amount_tests[:-1] # delete last row since its just the total
	amount_tests['Positivenanteil (%)'] = (amount_tests['Positiv getestet'] / amount_tests['Anzahl Testungen']) * 100.0

	amount_tests[['Meldewoche', 'Meldejahr']]		= amount_tests['Kalenderwoche'].str.split('/', expand=True)

	amount_tests = date_col(amount_tests)

	amount_tests.drop(columns=['Kalenderwoche', 'Anzahl übermittelnder Labore'], inplace=True)
	amount_tests.to_csv(data_dir + 'amount_tests.csv', index=False)

def collect_vaccinations():
	global populations

	# vaccinations
	vaccinations = download_data(vaccinations_url, sep='\t', header=0)

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

def collect_vaccinations_by_state():
	vaxx_by_state = download_data(vaxx_rate_url, sheet=1, header=[0, 1, 2], nrows=16)
	case_incidence_by_state = download_data(cases_by_state_url, sheet=4, header=2, nrows=16).dropna(axis=1)
	hospitalizations_incidence_by_state = download_data(cases_by_state_url, sheet=2, header=2, nrows=16).dropna(axis=1)

	vaxx_rate = {}
	vaxx_rate['state'] = vaxx_by_state['Bundesland', 'Unnamed: 1_level_1', 'Unnamed: 1_level_2']
	vaxx_rate['fully_vaccinated'] = vaxx_by_state['Impfquote grundimmunisiert', 'Gesamt-bevölkerung*', 'Unnamed: 13_level_2']
	vaxx_rate['boostered'] = vaxx_by_state['Impfquote Auffrischimpfung', 'Gesamt-bevölkerung*', 'Unnamed: 20_level_2']
	vaxx_rate['case_incidence'] = case_incidence_by_state[case_incidence_by_state.columns[-1]]
	vaxx_rate['hospitalization_incidence'] = hospitalizations_incidence_by_state[hospitalizations_incidence_by_state.columns[-1]]
	vaxx_rate['hosp_per_case_incidence'] = vaxx_rate['case_incidence'] / vaxx_rate['hospitalization_incidence']

	vaxx_rate = pd.DataFrame.from_dict(vaxx_rate)

	vaxx_rate.to_csv(data_dir + 'vaxx_rate_by_state.csv', index=False)
	
def main():
	global populations
	populations	= pd.read_csv(data_dir + 'population.csv')
	collect_daily_cases()
	collect_cases()
	collect_hospitalizations()
	collect_deaths()
	collect_tests()
	collect_vaccinations()
	collect_vaccinations_by_state()

if __name__ == '__main__':
	main()