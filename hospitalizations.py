import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

def plot_hospitalizations(hospitalizations_total, hospitalizations_age, hospitalizations_age_incidence):
	# Create plot for hospitalizations (total and rate)
	fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

	colors = plt.cm.tab10

	ax1.set_title('Hospitalizations for CoViD-19 in Germany')
	ax1.set_ylabel('Hospitalizations')

	# TODO: get age groups programmatically

	# plot total hospitalizations for all age groups
	ax1.plot(hospitalizations_total['Meldedatum'], hospitalizations_total['Anzahl hospitalisiert'], label='Total')
	ax1.stackplot(
		hospitalizations_age['Meldedatum'], 
		hospitalizations_age['Fälle A00..04'], hospitalizations_age['Fälle A05..14'], hospitalizations_age['Fälle A15..34'],
		hospitalizations_age['Fälle A35..59'], hospitalizations_age['Fälle A60..79'], hospitalizations_age['Fälle A80+'],
		labels=['0-4', '5-14', '15-34', '35-59', '60-79', '80+'],
		colors=[colors(i) for i in range(1,7)]
	)
	#ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A80+'], label='80+')
	#ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A60..79'], label='60-79')
	#ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A35..59'], label='35-59')
	#ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A15..34'], label='15-34')
	#ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A05..14'], label='5-14')
	#ax1.plot(hospitalizations_age['Meldedatum'], hospitalizations_age['Fälle A00..04'], label='0-4')

	ax1.legend()

	ax2.set_ylabel('Hospitalization Incidence')
	ax2.set_xlabel('Year-Calendar Week')

	# plot hospitalization incidence for all age groups
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A80+'], color=colors(6), label='80+')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A60..79'], color=colors(5), label='60-79')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A35..59'], color=colors(4), label='35-59')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A15..34'], color=colors(3), label='15-34')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A05..14'], color=colors(2), label='5-14')
	ax2.plot(hospitalizations_age_incidence['Meldedatum'], hospitalizations_age_incidence['Inzidenz A00..04'], color=colors(1), label='0-4')

	ax2.legend()

	# TODO: segment plot into months instead of having week-ticks
	# rotate x labels for readability
	plt.xticks(rotation=45, ha='right')
	# Keep every 2nd label for readability
	n = 2  
	[l.set_visible(False) for (i,l) in enumerate(ax2.xaxis.get_ticklabels()) if i % n != 0]

	plt.show()