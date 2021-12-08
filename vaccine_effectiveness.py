import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

def plot_hospitalization_rate(hospitalizations_total, cases):
	fig, ax = plt.subplots()

	ax.set_title('Hospitalization per infection')
	ax.set_ylabel('Hospitalization rate')
	ax.set_xlabel('Year-Calendar Week')

	ax.plot(cases['Meldedatum'], (hospitalizations_total['Anzahl hospitalisiert'] / cases['Gesamt']) * 100.0, label='Hosp. Rate')

	ax.legend()

	plt.xticks(rotation=45, ha='right')
	# Keep every 2nd label for readability
	n = 2  
	[l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
	plt.show()