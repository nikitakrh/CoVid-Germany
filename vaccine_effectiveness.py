import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

def plot_hospitalization_rate(hospitalizations_total, cases, vaccinations):
	fig, ax1 = plt.subplots()

	ax1.set_title('Hospitalization per infection')
	ax1.set_xlabel('Year-Calendar Week')

	ax2 = ax1.twinx()

	ax1.set_ylabel('Hospitalization rate in %')
	ax2.set_ylabel('Vaccination Rate in %')

	ax2.set_ylim([0,100])

	colors = ['xkcd:blue', 'xkcd:light green', 'xkcd:green']

	p1, = ax1.plot(cases['Meldedatum'], (hospitalizations_total['Anzahl hospitalisiert'] / cases['Gesamt']) * 100.0, color=colors[0], label='Hosp. Rate')
	p2, = ax2.plot(vaccinations['Meldedatum'], vaccinations['fully vaccinated'], color=colors[1], label='fully vaccinated')
	p3, = ax2.plot(vaccinations['Meldedatum'], vaccinations['boostered'], color=colors[2], label='boostered')

	lns = [p1, p2, p3]
	ax1.legend(handles=lns, loc='best')

	ax1.yaxis.label.set_color(p1.get_color())
	ax2.yaxis.label.set_color(p2.get_color())

	fig.tight_layout()

	# TODO: segment plot into months instead of having week-ticks
	# rotate x labels for readability
	plt.draw()
	ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
	# Keep every 2nd label for readability
	n = 2  
	[l.set_visible(False) for (i,l) in enumerate(ax1.xaxis.get_ticklabels()) if i % n != 0]
	plt.show()