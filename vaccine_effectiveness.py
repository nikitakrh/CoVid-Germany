import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_hospitalization_rate(hospitalizations_total, cases, vaccinations):

	fig = make_subplots(specs=[[{'secondary_y': True}]])

	fig.add_trace(
		go.Scatter(x=cases['Meldedatum'], y=(hospitalizations_total['Anzahl hospitalisiert'] / cases['Gesamt']) * 100.0, name='Hosp. Rate'),
		secondary_y=False
	)

	fig.add_trace(
		go.Scatter(x=vaccinations['Meldedatum'], y=vaccinations['fully vaccinated'], name='fully vaccinated'),
		secondary_y=True
	)

	fig.add_trace(
		go.Scatter(x=vaccinations['Meldedatum'], y=vaccinations['boostered'], name='boostered'),
		secondary_y=True
	)

	return fig