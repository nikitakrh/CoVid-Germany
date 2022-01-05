# pandas for data processing
import pandas as pd
import numpy as np
import os

# import other files for plotting
from cases import plot_cases, plot_cases_by_age, plot_cases_positivityrate
from deaths import plot_deaths, plot_deaths_by_age
from hospitalizations import plot_hospitalizations, plot_hospitalizations_by_age
from vaccine_effectiveness import plot_hospitalization_rate
from util.helper import collect_data

# files and directories
data_dir = os.path.join(os.path.dirname(__file__), 'data/')

# figure dictionary
figs = {}

def create_plots():
	# get newest data and save it in own csv format
	collect_data()

	# ------------------------------
	# ------- PREPROCESSING --------
	# ------------------------------

	# get DataFrames from excel files
	# population by age(groups)
	populations				= pd.read_csv(data_dir + 'population.csv')
	# cases
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

	return figs