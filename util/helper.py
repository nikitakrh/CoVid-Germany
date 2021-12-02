import pandas as pd

def date_col(df, year_col, week_col):
	df[year_col] = df[year_col].astype(str)
	df[week_col] = df[week_col].astype(str)
	df['Meldedatum'] = df[year_col] + '-' + df[week_col]
	df.drop(columns=[year_col, week_col], inplace=True)
	return df