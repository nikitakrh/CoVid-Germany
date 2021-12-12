import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# TODO: plot cases and hospitalizations by age for each agegroup

def plot_cases(cases, cases_incidence):
	fig_cases_total = px.line(
		cases, x='Meldedatum', y='Gesamt', 
		title='Cases of CoViD', labels={'Meldedatum': 'Date', 'Gesamt': 'Cases'}
	)

	fig_cases_incidence_total = px.line(
		cases_incidence, x='Meldedatum', y='Gesamt',
		title='Case Incidence of CoViD', labels={'Meldedatum': 'Date', 'Gesamt': 'Total Case Incidence'}
	)

	return fig_cases_total, fig_cases_incidence_total

def plot_cases_by_age(cases, cases_incidence):
	fig_cases_by_age = px.area(
		cases,
		x='Meldedatum',
		y=['Fälle A00..04', 'Fälle A05..14', 'Fälle A15..34', 'Fälle A35..59', 'Fälle A60..79', 'Fälle A80+'],
	)

	fig_cases_incidence_by_age= px.line(
		cases_incidence, 
		x='Meldedatum', 
		y=['Inzidenz A00..04', 'Inzidenz A05..14','Inzidenz A15..34', 'Inzidenz A35..59', 'Inzidenz A60..79', 'Inzidenz A80+'], 
		title='Case Incidence by Age',
		labels={'Meldedatum': 'Date', 'value': 'Case Incidence', 'variable': 'Agegroups'}
	)

	return fig_cases_by_age, fig_cases_incidence_by_age

def plot_cases_positivityrate(cases, amount_tests):
	fig_test_positivity_rate = make_subplots(specs=[[{'secondary_y': True}]])

	fig_test_positivity_rate.add_trace(
		go.Scatter(x=cases['Meldedatum'], y=cases['Gesamt'], name='Total Cases'),
		secondary_y=False
	)

	fig_test_positivity_rate.add_trace(
		go.Scatter(x=amount_tests['Meldedatum'], y=amount_tests['Positivenanteil (%)'], name='Positive Test Rate'),
		secondary_y=True
	)

	fig_test_positivity_rate.update_yaxes(showgrid=False, secondary_y=True)

	return fig_test_positivity_rate