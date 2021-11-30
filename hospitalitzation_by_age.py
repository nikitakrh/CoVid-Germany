import pandas as pd 
import numpy as np
import os
import matplotlib.pyplot as plt

data_dir = os.path.join(os.path.dirname(__file__), 'data/')
clinical_filename = 'Klinische_Aspekte.xlsx'

def main():
	hospitalizations_total = pd.read_excel(data_dir + clinical_filename, sheet_name=0, header=3)

	# Create column for calendar week
	hospitalizations_total['Meldejahr'] = hospitalizations_total['Meldejahr'].astype(str)
	hospitalizations_total['MW'] = hospitalizations_total['MW'].astype(str)
	hospitalizations_total['Meldedatum'] = hospitalizations_total['Meldejahr'] + '-' + hospitalizations_total['MW']
	hospitalizations_total.drop(columns=['Meldejahr', 'MW'])

	# Create plot for hospitalizations (total and rate)
	fig, ax = plt.subplots()

	ax.plot(hospitalizations_total['Meldedatum'], hospitalizations_total['Anzahl hospitalisiert'])


	plt.xticks(rotation=45)
	plt.show()


if __name__ == '__main__':
	main()