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
	plt.show()