import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# TODO: plot cases and hospitalizations by age for each agegroup

def plot_cases(cases, cases_incidence):
	fig_cases_total = px.line(
		cases, x='Meldedatum', y='Gesamt', 
		title='Cases of CoViD', 
		labels={'Meldedatum': 'Date', 'Gesamt': 'Cases'}
	)

	fig_cases_incidence_total = px.line(
		cases_incidence, x='Meldedatum', y='Gesamt',
		title='Case Incidence of CoViD', 
		labels={'Meldedatum': 'Date', 'Gesamt': 'Case Incidence'}
	)

	return fig_cases_total, fig_cases_incidence_total

def plot_cases_by_age(cases, cases_incidence):
	fig_cases_by_age = px.area(
		cases,
		x='Meldedatum',
		y=['Cases 0-4y', 'Cases 5-14y', 'Cases 15-34y', 'Cases 35-59y', 'Cases 60-79y', 'Cases 80+y'],
		title='Cases by Age',
		labels={'Meldedatum': 'Date', 'value': 'Cases', 'variable': 'Agegroups'}
	)

	fig_cases_incidence_by_age= px.line(
		cases_incidence, 
		x='Meldedatum', 
		y=['Incidence 0-4y', 'Incidence 5-14y','Incidence 15-34y', 'Incidence 35-59y', 'Incidence 60-79y', 'Incidence 80+y'], 
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

	fig_test_positivity_rate.update_layout(title_text='Comparison: Cases vs. Test Positivity Rate')
	fig_test_positivity_rate.update_xaxes(title_text='Date')
	fig_test_positivity_rate.update_yaxes(title_text='Cases', secondary_y=False)
	fig_test_positivity_rate.update_yaxes(title_text='Test Positivity Rate (%)', showgrid=False, secondary_y=True)

	return fig_test_positivity_rate