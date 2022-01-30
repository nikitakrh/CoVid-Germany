import plotly.express as px

def plot_hospitalizations(hospitalizations):
	fig_hosp_total = px.line(
		hospitalizations, x='Meldedatum', y='Total Cases', 
		title='Hospitalizations for CoViD-19 in Germany',
		labels={'Meldedatum': 'Date', 'Fälle Gesamt': 'Hospitalizations'}
	)
	fig_hosp_incidence_total = px.line(
		hospitalizations, x='Meldedatum', y='Total Incidence',
		title='Hospitalization Incidence', labels={'Meldedatum': 'Date', 'Total Incidence': 'Hospitalization Incidence'}
	)
	
	return fig_hosp_total, fig_hosp_incidence_total

def plot_hospitalizations_by_age(hospitalizations):
	# TODO: get age groups programmatically
	fig_hosp_by_age = px.area(
		hospitalizations, 
		x='Meldedatum',
		y=['Cases 0-4y', 'Cases 5-14y', 'Cases 15-34y', 'Cases 35-59y', 'Cases 60-79y', 'Cases 80+y'],
		title='Hospitalizations by Age',
		labels={'Meldedatum': 'Date', 'value': 'Hospitalization Incidence', 'variable': 'Agegroups'}

	)
	fig_hosp_incidence_by_age = px.line(
		hospitalizations, 
		x='Meldedatum', 
		y=['Incidence 0-4y', 'Incidence 5-14y','Incidence 15-34y', 'Incidence 35-59y', 'Incidence 60-79y', 'Incidence 80+y'], 
		title='Hospitalization Incidence by Age',
		labels={'Meldedatum': 'Date', 'value': 'Hospitalization Incidence', 'variable': 'Agegroups'}
	)

	return fig_hosp_by_age, fig_hosp_incidence_by_age