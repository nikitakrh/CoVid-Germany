import pandas as pd 
import numpy as np
import os
import matplotlib.pyplot as plt

from util.helper import date_col

def plot_hospitalizations(hospitalizations_total, hospitalizations_age, hospitalizations_age_incidence):
	# Create plot for hospitalizations (total and rate)
	fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

	ax1.set_title('Hospitalizations for CoViD-19 in Germany')
	ax1.set_ylabel('Hospitalizations')

	# TODO: get age groups programmatically

	# plot total hospitalizations for all age groups
	# TODO: plot stacked
	ax1.plot(hospitalizations_total['Meldedatum'], hospitalizations_total['Anzahl hospitalisiert'], label='Total')
	ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A80+'], label='80+')
	ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A60..79'], label='60-79')
	ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A35..59'], label='35-59')
	ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A15..34'], label='15-34')
	ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A05..14'], label='5-14')
	ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A00..04'], label='0-4')

	ax1.legend()

	ax2.set_ylabel('Hospitalization Incidence')
	ax2.set_xlabel('Year-Calendar Week')

	# TODO: change color coding to match with upper graph
	# plot hospitalization incidence for all age groups
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A80+'], label='80+')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A60..79'], label='60-79')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A35..59'], label='35-59')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A15..34'], label='15-34')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A05..14'], label='5-14')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A00..04'], label='0-4')

	ax2.legend()

	# TODO: segment plot into months instead of having week-ticks
	# rotate x labels for readability
	plt.xticks(rotation=45, ha='right')
	# Keep every 2nd label for readability
	n = 2  
	[l.set_visible(False) for (i,l) in enumerate(ax2.xaxis.get_ticklabels()) if i % n != 0]

	plt.show()