# module imports
# dash for frontend dashboard
import dash
from dash import dcc
from dash import html

# pandas for data processing
import pandas as pd
import os

# import other files for plotting
from hospitalizations import plot_hospitalizations
from cases import plot_cases_by_age, plot_cases_positivityrate
from vaccine_effectiveness import plot_hospitalization_rate
from util.helper import collect_data, date_col, date_to_week

# files and directories
data_dir = os.path.join(os.path.dirname(__file__), 'data/')
clinical_filename = 'Klinische_Aspekte.xlsx'
cases_filename = 'Altersverteilung.xlsx'
amount_tests_filename = 'Testzahlen-gesamt.xlsx'
vaccinations_filename = 'germany_vaccinations_timeseries_v2.tsv'
populations_filename = 'Bevoelkerung_Altersgruppen.csv'

def main():
	app = dash.Dash(__name__)

	# ------------------------------
	# ------- PREPROCESSING --------
	# ------------------------------
	collect_data()

	# get DataFrames from excel files
	# population by age(groups)
	populations = pd.read_csv(data_dir + populations_filename, sep=';', header=0, index_col='Alter', encoding='latin-1')
	# hospitalizations
	hospitalizations_total = pd.read_excel(data_dir + clinical_filename, sheet_name=0, header=3, engine='openpyxl')
	hospitalizations_age = pd.read_excel(data_dir + clinical_filename, sheet_name=2, header=5, engine='openpyxl')
	# cases
	cases = pd.read_excel(data_dir + cases_filename, sheet_name=0, header=0, index_col='Altersgruppe', engine='openpyxl')
	cases_incidence = pd.read_excel(data_dir + cases_filename, sheet_name=1, header=0, index_col='Altersgruppe', engine='openpyxl')
	# amount of tests
	amount_tests = pd.read_excel(data_dir + amount_tests_filename, sheet_name=1, header=0, engine='openpyxl')
	# vaccinations
	vaccinations = pd.read_csv(data_dir + vaccinations_filename, sep='\t', header=0)

	# DataFrame-/file-specific preprocessing
	# consistent age groups in population DataFrame
	total_population = populations['31.12.2020'].sum()
	populations = populations.T.reset_index()
	populations['A00..04'] = populations['unter 1 Jahr']
	populations['A00..04'] += sum([populations[f'{i}-Jährige'] for i in range(1,5)])
	populations['A05..14'] = sum([populations[f'{i}-Jährige'] for i in range(5,15)])
	populations['A15..34'] = sum([populations[f'{i}-Jährige'] for i in range(15,35)])
	populations['A35..59'] = sum([populations[f'{i}-Jährige'] for i in range(35,60)])
	populations['A60..79'] = sum([populations[f'{i}-Jährige'] for i in range(60,80)])
	populations['A80+'] = sum([populations[f'{i}-Jährige'] for i in range(80,85)])
	populations['A80+'] += populations['85 Jahre und mehr']

	# interpolate missing values
	hospitalizations_age = hospitalizations_age.interpolate(method='linear')
	# add hospitalization incidence
	hospitalizations_age['Inzidenz A00..04'] = (hospitalizations_age['Fälle A00..04'] / populations.at[0,'A00..04']) * 100000.0
	hospitalizations_age['Inzidenz A05..14'] = (hospitalizations_age['Fälle A05..14'] / populations.at[0,'A05..14']) * 100000.0
	hospitalizations_age['Inzidenz A15..34'] = (hospitalizations_age['Fälle A15..34'] / populations.at[0,'A15..34']) * 100000.0
	hospitalizations_age['Inzidenz A35..59'] = (hospitalizations_age['Fälle A35..59'] / populations.at[0,'A35..59']) * 100000.0
	hospitalizations_age['Inzidenz A60..79'] = (hospitalizations_age['Fälle A60..79'] / populations.at[0,'A60..79']) * 100000.0
	hospitalizations_age['Inzidenz A80+'] = (hospitalizations_age['Fälle A80+'] / populations.at[0,'A80+']) * 100000.0
	# transpose cases DataFrames
	cases = cases.T.reset_index()
	cases_incidence = cases_incidence.T.reset_index()
	# generate new age groups
	cases['Fälle A00..04'] = cases['0 - 4']
	cases['Fälle A05..14'] = cases['5 - 9'] + cases['10 - 14']
	cases['Fälle A15..34'] = cases['15 - 19'] + cases['20 - 24'] + cases['25 - 29'] + cases['30 - 34']
	cases['Fälle A35..59'] = cases['35 - 39'] + cases['40 - 44'] + cases['45 - 49'] + cases['50 - 54'] + cases['55 - 59']
	cases['Fälle A60..79'] = cases['60 - 64'] + cases['65 - 69'] + cases['70 - 74'] + cases['75 - 79']
	cases['Fälle A80+'] = cases['80 - 84'] + cases['85 - 89'] + cases['90+']
	cases_incidence['Inzidenz A00..04'] = (cases['Fälle A00..04'] / populations.at[0,'A00..04']) * 100000.0
	cases_incidence['Inzidenz A05..14'] = (cases['Fälle A05..14'] / populations.at[0,'A05..14']) * 100000.0
	cases_incidence['Inzidenz A15..34'] = (cases['Fälle A15..34'] / populations.at[0,'A15..34']) * 100000.0
	cases_incidence['Inzidenz A35..59'] = (cases['Fälle A35..59'] / populations.at[0,'A35..59']) * 100000.0
	cases_incidence['Inzidenz A60..79'] = (cases['Fälle A60..79'] / populations.at[0,'A60..79']) * 100000.0
	cases_incidence['Inzidenz A80+'] = (cases['Fälle A80+'] / populations.at[0,'A80+']) * 100000.0
	# clean up amount_test DataFrame
	amount_tests.at[0, 'Kalenderwoche'] = '10/2020'
	amount_tests = amount_tests[:-1] # delete last row since its just the total
	amount_tests['Positivenanteil (%)'] = (amount_tests['Positiv getestet'] / amount_tests['Anzahl Testungen']) * 100.0
	# add 'fully vaccinated' and 'boostered' column into vaccination DataFrame
	vaccinations['fully vaccinated'] = ((
		vaccinations['dosen_biontech_zweit_kumulativ'] + 
		vaccinations['dosen_moderna_zweit_kumulativ'] + 
		vaccinations['dosen_astra_zweit_kumulativ'] + 
		vaccinations['dosen_johnson_erst_kumulativ']
	) / total_population) * 100.0
	vaccinations['boostered'] = ((
		vaccinations['dosen_biontech_dritt_kumulativ'] +
		vaccinations['dosen_moderna_dritt_kumulativ'] + 
		vaccinations['dosen_astra_dritt_kumulativ'] + 
		vaccinations['dosen_johnson_zweit_kumulativ'] + 
		vaccinations['dosen_johnson_dritt_kumulativ']
	) / total_population) * 100.0
	# adjust vaccination DataFrame to have week column
	vaccinations = date_to_week(vaccinations)
	vaccinations = vaccinations.groupby(['Meldejahr', 'Meldewoche']).max().reset_index()

	# create new columns for better processing
	cases[['Meldejahr', 'Meldewoche']] = cases['index'].str.split('_', expand=True)
	cases_incidence[['Meldejahr', 'Meldewoche']] = cases_incidence['index'].str.split('_', expand=True)
	amount_tests[['Meldewoche', 'Meldejahr']] = amount_tests['Kalenderwoche'].str.split('/', expand=True)

	# create column for calendar week
	hospitalizations_total = date_col(hospitalizations_total, week_col='MW')
	hospitalizations_age = date_col(hospitalizations_age)
	cases = date_col(cases)
	cases_incidence = date_col(cases_incidence)
	amount_tests = date_col(amount_tests)
	vaccinations = date_col(vaccinations)

	# ------------------------------
	# --------- PLOT DATA ----------
	# ------------------------------

	# create plots
	figs_hosp = plot_hospitalizations(hospitalizations_total, hospitalizations_age)
	figs_cases = plot_cases_by_age(cases, cases_incidence)
	#fig_pos = plot_cases_positivityrate(cases, amount_tests)
	#fig_hosp_rate = plot_hospitalization_rate(hospitalizations_total, cases, vaccinations)
	


	# ------------------------------
	# --------- APP LAYOUT ---------
	# ------------------------------
	colors = {
		'background': '#121212',
		'text': '#BB86FC'
	}
	for fig in (figs_hosp + figs_cases):
		fig = style_fig(fig, colors)

	app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
		html.H1(
			children='CoViD Germany',
			style={
				'color': colors['text'],
				'textAlign': 'center',
			}),

		html.Div(
			children='Custom dashboard about corona infections, hospitalizations and vaccinations in Germany',
			style={
				'color': colors['text'],
				'textAlign': 'center',
				}),

		html.Div(children=[
			html.H2(
				children='Hospitalizations',
				style={
					'color': colors['text'],
				}),

			dcc.Graph(
				id='hospitalizations',
				figure=figs_hosp[0]
			),

			dcc.Graph(
				id='hosp-incidence',
				figure=figs_hosp[1]
			),
		]),

		html.Div(children=[
			html.H2(
				children='Cases',
				style={
					'color': colors['text'],
				}),

			dcc.Graph(
				id='cases',
				figure=figs_cases[0]
			),

			dcc.Graph(
				id='case-incidence',
				figure=figs_cases[1]
			)
		]),
	])

	app.run_server(debug=True)

def style_fig(fig, colors):
	fig.update_layout(
		plot_bgcolor=colors['background'],
		paper_bgcolor=colors['background'],
		font_color=colors['text']
	)
	pass

if __name__ == '__main__':
	main()