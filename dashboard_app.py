# module imports
# dash for frontend dashboard
import dash
from dash import dcc
from dash import html

from create_plots import create_plots
from util.helper import style_fig

def main():
	figs = create_plots()
	# ------------------------------
	# --------- APP LAYOUT ---------
	# ------------------------------
	app = dash.Dash(__name__)
	colors = {
		'background': '#121212',
		'text': '#BB86FC'
	}
	for fig in figs.values():
		fig = style_fig(fig, colors)

	app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
		html.H1(
			children='CoViD Germany',
			style={
				'color': colors['text'],
				'textAlign': 'center',
			}
		),

		html.Div(
			children='Custom dashboard about corona infections, hospitalizations and vaccinations in Germany',
			style={
				'color': colors['text'],
				'textAlign': 'center',
				}
		),

		# Total numbers side by side
		html.Div(children=[
			html.H2(
				children='Total',
				style={
					'color': colors['text'],
				}
			),

			# Total Cases
			html.Div(children=[
				dcc.Graph(
					id='cases-total',
					figure=figs['cases-total']
				),
				dcc.Graph(
					id='cases-incidence-total',
					figure=figs['cases-incidence-total']
				)
			],
			style={
					'width': '33%',
					'display': 'inline-block',
			}),

			# Total Hospitalizations
			html.Div(children=[
				dcc.Graph(
					id='hosp-total',
					figure=figs['hosp-total']
				),
				dcc.Graph(
					id='hosp-incidence-total',
					figure=figs['hosp-incidence-total']
				)
			],
			style={
					'width': '33%',
					'display': 'inline-block',
			}),

		]),

		# Age breakdown side by side
		html.Div(children=[
			html.H2(
				children='By Age',
				style={
					'color': colors['text'],
				}
			),	

			# cases by age
			html.Div(children=[
				dcc.Graph(
					id='cases-by-age',
					figure=figs['cases-by-age']
				),
				dcc.Graph(
					id='cases-incidence-by-age',
					figure=figs['cases-incidence-by-age']
				),
				],
				style={
					'width': '33%',
					'display': 'inline-block',
				}
			),

			# hospitalizations by age
			html.Div(children=[
				dcc.Graph(
					id='hosp-by-age',
					figure=figs['hosp-by-age']
				),
				dcc.Graph(
					id='hosp-incidence-by-age',
					figure=figs['hosp-incidence-by-age']
				),
				],
				style={
					'width': '33%',
					'display': 'inline-block',
				}
			),
		]),

		html.Div(children=[
			html.H2(
				children='Additional Information',
				style={
					'color': colors['text']
				}
			),

			dcc.Graph(
				id='test-positivity-rate',
				figure=figs['test-positivity-rate']
			),

			dcc.Graph(
				id='hosp-rate',
				figure=figs['hosp-rate']
			)
		]),
	])

	app.run_server(debug=True)

if __name__ == '__main__':
	main()