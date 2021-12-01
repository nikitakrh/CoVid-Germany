import pandas as pd 
import numpy as np
import os
import matplotlib.pyplot as plt

data_dir = os.path.join(os.path.dirname(__file__), 'data/')
clinical_filename = 'Klinische_Aspekte.xlsx'

def date_col(df, year_col, week_col):
	df[year_col] = df[year_col].astype(str)
	df[week_col] = df[week_col].astype(str)
	df['Meldedatum'] = df[year_col] + '-' + df[week_col]
	df.drop(columns=[year_col, week_col], inplace=True)
	return df

def main():
	hospitalizations_total = pd.read_excel(data_dir + clinical_filename, sheet_name=0, header=3)
	hospitalizations_age = pd.read_excel(data_dir + clinical_filename, sheet_name=2, header=5)
	hospitalizations_age_incidence = pd.read_excel(data_dir + clinical_filename, sheet_name=4, header=4)

	# Create column for calendar week
	hospitalizations_total = date_col(hospitalizations_total, 'Meldejahr', 'MW')
	hospitalizations_age = date_col(hospitalizations_age, 'Meldejahr', 'Meldewoche')
	hospitalizations_age_incidence = date_col(hospitalizations_age_incidence, 'Meldejahr', 'Meldewoche')

	# Create plot for hospitalizations (total and rate)
	fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

	ax1.set_title('Hospitalizations for CoViD-19 in Germany')
	ax1.set_ylabel('Hospitalizations')

	ax1.plot(hospitalizations_total['Meldedatum'], hospitalizations_total['Anzahl hospitalisiert'], label='Total')
	ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A80+'], label='80+')
	ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A60..79'], label='60-79')
	ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A35..59'], label='35-59')
	ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A15..34'], label='15-34')
	ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A05..14'], label='5-14')
	ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A00..04'], label='0-4')

	ax1.legend()

	ax2.set_ylabel('Hospitalization Incidence')
	ax2.set_xlabel('Year-Calendar Week')

	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A80+'], label='80+')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A60..79'], label='60-79')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A35..59'], label='35-59')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A15..34'], label='15-34')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A05..14'], label='5-14')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A00..04'], label='0-4')

	ax2.legend()

	plt.xticks(rotation=45)
	n = 2  # Keeps every 2nd label
	[l.set_visible(False) for (i,l) in enumerate(ax1.xaxis.get_ticklabels()) if i % n != 0]

	plt.show()


if __name__ == '__main__':
	main()