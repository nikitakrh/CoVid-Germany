import plotly.express as px

def plot_hospitalizations(hospitalizations_total, hospitalizations_age):

	# TODO: get age groups programmatically
	fig1 = px.line(
		hospitalizations_total, x='Meldedatum', y='Anzahl hospitalisiert', 
		title='Hospitalizations for CoViD-19 in Germany',
		labels={'Meldedatum': 'Date'}
	)
	fig1.add_traces(
		list(px.area(
			hospitalizations_age, 
			x='Meldedatum',
			y=['Fälle A00..04', 'Fälle A05..14','Fälle A15..34', 'Fälle A35..59', 'Fälle A60..79', 'Fälle A80+']
		).select_traces())
	)

	fig2 = px.line(
		hospitalizations_age, 
		x='Meldedatum', 
		y=['Inzidenz A00..04', 'Inzidenz A05..14','Inzidenz A15..34', 'Inzidenz A35..59', 'Inzidenz A60..79', 'Inzidenz A80+'], 
		title='Hospitalization Incidence by Age',
		labels={'Meldedatum': 'Date', 'value': 'Hospitalization Incidence', 'variable': 'Agegroups'}
	)

	figs = [fig1, fig2]
	return figs