import plotly.express as px

def plot_deaths(deaths):
	fig_deaths_total = px.line(
		deaths, x='Meldedatum', y='Fälle Gesamt',
		title='Deaths due to CoViD'
	)

	fig_deaths_incidence_total = px.line(
		deaths, x='Meldedatum', y='Inzidenz Gesamt',
		title='Death Incidence'
	)

	return fig_deaths_total, fig_deaths_incidence_total

def plot_deaths_by_age(deaths):
	fig_deaths_by_age = px.area(
		deaths,
		x='Meldedatum',
		y=['Fälle A00..19', 'Fälle A20..59', 'Fälle A60..79', 'Fälle A80+'],
	)

	fig_deaths_incidence_by_age= px.line(
		deaths, 
		x='Meldedatum', 
		y=['Inzidenz A00..19', 'Inzidenz A20..59', 'Inzidenz A60..79', 'Inzidenz A80+'], 
		title='Death Incidence by Age',
		labels={'Meldedatum': 'Date', 'value': 'Case Incidence', 'variable': 'Agegroups'}
	)

	return fig_deaths_by_age, fig_deaths_incidence_by_age
