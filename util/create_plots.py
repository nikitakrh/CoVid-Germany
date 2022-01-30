# pandas for data processing
import pandas as pd
import numpy as np
import os

# import other files for plotting
from util.plots.cases import plot_cases, plot_cases_by_age, plot_cases_positivityrate, predict_next_30_days
from util.plots.deaths import plot_deaths, plot_deaths_by_age
from util.plots.hospitalizations import plot_hospitalizations, plot_hospitalizations_by_age
from util.plots.vaccine_effectiveness import plot_hospitalization_rate, plot_cases_vs_vaxx_rate, plot_hosp_vs_vaxx_rate, plot_hosp_per_cases_vs_vaxx_rate

# files and directories
util_dir = os.path.dirname(__file__)
data_dir = os.path.join(os.path.join(util_dir, os.pardir), 'data/')

# figure dictionary
figs = {}

def create_plots():
	# get DataFrames from excel files
	# population by age(groups)
	populations				= pd.read_csv(data_dir + 'population.csv')
	# cases
	daily_cases				= pd.read_csv(data_dir + 'daily_cases.csv')
	cases					= pd.read_csv(data_dir + 'cases.csv')
	cases_incidence			= pd.read_csv(data_dir + 'cases_incidence.csv')
	# hospitalizations
	hospitalizations		= pd.read_csv(data_dir + 'hospitalizations.csv')
	# deaths
	deaths					= pd.read_csv(data_dir + 'deaths.csv')
	# amount of tests
	amount_tests			= pd.read_csv(data_dir + 'amount_tests.csv')
	# vaccinations
	vaccinations			= pd.read_csv(data_dir + 'vaccinations.csv')
	# vaxx rate by state
	vaxx_rate_by_state		= pd.read_csv(data_dir + 'vaxx_rate_by_state.csv')

	# ------------------------------
	# --------- PLOT DATA ----------
	# ------------------------------
	# create plots
	figs['cases-total'], figs['cases-incidence-total']		= plot_cases(cases, cases_incidence)
	figs['cases-by-age'], figs['cases-incidence-by-age']	= plot_cases_by_age(cases, cases_incidence)
	figs['hosp-total'], figs['hosp-incidence-total']		= plot_hospitalizations(hospitalizations)
	figs['hosp-by-age'], figs['hosp-incidence-by-age']		= plot_hospitalizations_by_age(hospitalizations)
	figs['deaths-total'], figs['deaths-incidence-total']	= plot_deaths(deaths)
	figs['deaths-by-age'], figs['deaths-incidence-by-age']	= plot_deaths_by_age(deaths)
	figs['test-positivity-rate']							= plot_cases_positivityrate(cases, amount_tests)
	figs['hosp-rate']										= plot_hospitalization_rate(hospitalizations, cases, vaccinations)
	figs['case-vs-vaxx-rate']								= plot_cases_vs_vaxx_rate(vaxx_rate_by_state)
	figs['hosp-vs-vaxx-rate']								= plot_hosp_vs_vaxx_rate(vaxx_rate_by_state)
	figs['hosp-per-cases-vs-vaxx-rate']						= plot_hosp_per_cases_vs_vaxx_rate(vaxx_rate_by_state)

	# ------------------------------
	# --------- PREDICTION ---------
	# ------------------------------
	figs['predicted-cases'] = predict_next_30_days(daily_cases)

	return figs