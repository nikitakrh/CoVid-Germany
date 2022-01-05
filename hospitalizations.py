import plotly.express as px

def plot_hospitalizations(hospitalizations):
	fig_hosp_total = px.line(
		hospitalizations, x='Meldedatum', y='Fälle Gesamt', 
		title='Hospitalizations for CoViD-19 in Germany',
		labels={'Meldedatum': 'Date'}
	)
	fig_hosp_incidence_total = px.line(
		hospitalizations, x='Meldedatum', y='Inzidenz Gesamt',
		title='Hospitalization Incidence', labels={'Meldedatum': 'Date'}
	)
	
	return fig_hosp_total, fig_hosp_incidence_total

def plot_hospitalizations_by_age(hospitalizations):
	# TODO: get age groups programmatically
	fig_hosp_by_age = px.area(
		hospitalizations, 
		x='Meldedatum',
		y=['Fälle A00..04', 'Fälle A05..14','Fälle A15..34', 'Fälle A35..59', 'Fälle A60..79', 'Fälle A80+']
	)
	fig_hosp_incidence_by_age = px.line(
		hospitalizations, 
		x='Meldedatum', 
		y=['Inzidenz A00..04', 'Inzidenz A05..14','Inzidenz A15..34', 'Inzidenz A35..59', 'Inzidenz A60..79', 'Inzidenz A80+'], 
		title='Hospitalization Incidence by Age',
		labels={'Meldedatum': 'Date', 'value': 'Hospitalization Incidence', 'variable': 'Agegroups'}
	)

	return fig_hosp_by_age, fig_hosp_incidence_by_age