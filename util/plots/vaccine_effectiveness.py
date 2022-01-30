import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_hospitalization_rate(hospitalizations, cases, vaccinations):

	fig_hosp_rate = make_subplots(specs=[[{'secondary_y': True}]])

	fig_hosp_rate.add_trace(
		go.Scatter(x=cases['Meldedatum'], y=(hospitalizations['Total Cases'] / cases['Gesamt']) * 100.0, name='Hosp. Rate'),
		secondary_y=False
	)

	fig_hosp_rate.add_trace(
		go.Scatter(x=vaccinations['Meldedatum'], y=vaccinations['fully vaccinated'], name='fully vaccinated'),
		secondary_y=True
	)

	fig_hosp_rate.add_trace(
		go.Scatter(x=vaccinations['Meldedatum'], y=vaccinations['boostered'], name='boostered'),
		secondary_y=True
	)

	fig_hosp_rate.update_layout(title_text='Comparison: Vaccination Rate vs. Hospitalization Rate')
	fig_hosp_rate.update_xaxes(title_text='Date')
	fig_hosp_rate.update_yaxes(title_text='Hospitalization Rate (%)', secondary_y=False)
	fig_hosp_rate.update_yaxes(title_text='Vaccination Progress (%)', showgrid=False, secondary_y=True)

	return fig_hosp_rate

def plot_cases_vs_vaxx_rate(vaxx_rate_by_state):
	fig_cases_vs_vaxx_rate = px.scatter(
			vaxx_rate_by_state, x='case_incidence', y='fully_vaccinated',
			size='case_incidence', text='state', trendline='ols'
		)

	return fig_cases_vs_vaxx_rate

def plot_hosp_vs_vaxx_rate(vaxx_rate_by_state):
	fig_hosp_vs_vaxx_rate = px.scatter(
			vaxx_rate_by_state, x='hospitalization_incidence', y='fully_vaccinated',
			size='hospitalization_incidence', text='state', trendline='ols'
		)

	return fig_hosp_vs_vaxx_rate

def plot_hosp_per_cases_vs_vaxx_rate(vaxx_rate_by_state):
	fig_hosp_per_cases_vs_vaxx_rate = px.scatter(
			vaxx_rate_by_state, x='hosp_per_case_incidence', y='fully_vaccinated',
			size='hosp_per_case_incidence', text='state', trendline='ols'
		)

	return fig_hosp_per_cases_vs_vaxx_rate