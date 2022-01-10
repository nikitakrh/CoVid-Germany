import plotly.express as px

def plot_deaths(deaths):
	fig_deaths_total = px.line(
		deaths, x='Meldedatum', y='Total Cases',
		title='Deaths due to CoViD',
		labels={'Meldedatum': 'Date', 'Total Cases': 'Deaths'}
	)

	fig_deaths_incidence_total = px.line(
		deaths, x='Meldedatum', y='Total Incidence',
		title='Death Incidence',
		labels={'Meldedatum': 'Date', 'Total Incidence': 'Death Incidence'}
	)

	return fig_deaths_total, fig_deaths_incidence_total

def plot_deaths_by_age(deaths):
	fig_deaths_by_age = px.area(
		deaths,
		x='Meldedatum',
		y=['Cases 0-19y', 'Cases 20-59y', 'Cases 60-79y', 'Cases 80+y'],
		title='Deaths by age',
		labels={'Meldedatum': 'Date', 'value': 'Deaths', 'variable': 'Agegroups'}
	)

	fig_deaths_incidence_by_age= px.line(
		deaths, 
		x='Meldedatum', 
		y=['Incidence 0-19y', 'Incidence 20-59y', 'Incidence 60-79y', 'Incidence 80+y'], 
		title='Death Incidence by Age',
		labels={'Meldedatum': 'Date', 'value': 'Death Incidence', 'variable': 'Agegroups'}
	)

	return fig_deaths_by_age, fig_deaths_incidence_by_age
