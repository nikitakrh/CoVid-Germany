import pandas as pd
import datetime


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

def collect_data():
	pass

def style_fig(fig, colors):
	fig.update_layout(
		plot_bgcolor=colors['tile'],
		paper_bgcolor=colors['background'],
		font_color=colors['text']
	)
	return fig