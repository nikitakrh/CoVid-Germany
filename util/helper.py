import pandas as pd


def date_col(df, year_col='Meldejahr', week_col='Meldewoche'):
	"""Creates the column 'Meldedatum' in the dataframe for uniform indexing of dataframes

	Keyword arguments:
	df -- DataFrame for which the column should be created
	year_col -- The name of the column in df that contains the year
	week_col -- The name of the column in df that contains the week number (1-52)
	"""
	df[year_col] = df[year_col].astype(str)
	df[week_col] = df[week_col].astype(str)
	df['Meldedatum'] = df[year_col] + '-' + df[week_col]
	df.drop(columns=[year_col, week_col], inplace=True)
	return df

def date_to_week(df, date_col='date'):
	pass

def collect_data():
	pass