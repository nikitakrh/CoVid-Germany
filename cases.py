import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

# TODO: plot cases and hospitalizations by age for each agegroup

def plot_cases_by_age(cases, cases_incidence):
	# Create plot for hospitalizations (total and rate)
	fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

	colors = plt.cm.tab10

	ax1.set_title('Cases of CoViD-19 in Germany')
	ax1.set_ylabel('Case')

	# TODO: get age groups programmatically

	# plot total number of cases for all age groups
	# TODO: plot stacked
	ax1.plot(cases['Meldedatum'], cases['Gesamt'], label='Total')
	ax1.stackplot(cases['Meldedatum'],
		cases['Fälle A00..04'], cases['Fälle A05..14'], cases['Fälle A15..34'],
		cases['Fälle A35..59'], cases['Fälle A60..79'], cases['Fälle A80+'],
		labels=['0-4', '5-14', '15-34', '35-59', '60-79', '80+'],
		colors=[colors(i) for i in range(1,7)]
		)

	ax1.legend()

	ax2.set_ylabel('Case Incidence by Age')
	ax2.set_xlabel('Year-Calendar Week')

	# plot case incidence for all age groups
	# TODO: case incidences with adjusted age groups
	ax2.plot(cases_incidence['Meldedatum'], cases_incidence['90+'], label='90+')
	for i in range(85, -1, -5):
		agegroup = str(i) + ' - ' + str(i+4)
		ax2.plot(cases_incidence['Meldedatum'], cases_incidence[agegroup], label=agegroup)

	ax2.legend()

	# TODO: segment plot into months instead of having week-ticks
	# rotate x labels for readability
	plt.xticks(rotation=45, ha='right')
	# Keep every 2nd label for readability
	n = 2  
	[l.set_visible(False) for (i,l) in enumerate(ax2.xaxis.get_ticklabels()) if i % n != 0]

	plt.show()

def plot_cases_positivityrate(cases, amount_tests):
	fig, ax1 = plt.subplots()
	ax1.set_title('Cases and Positive Test Rate')
	ax1.set_xlabel('Year-Calendar Week')

	ax2 = ax1.twinx()

	ax1.set_ylabel('Cases')
	ax2.set_ylabel('Positive Test Rate')

	color1 = 'blue'
	color2 = 'red'

	p1, = ax1.plot(cases['Meldedatum'], cases['Gesamt'], color=color1, label='Total Cases')
	p2, = ax2.plot(amount_tests['Meldedatum'], amount_tests['Positivenanteil (%)'], color=color2, label='Positive Test Rate')

	lns = [p1, p2]
	ax1.legend(handles=lns, loc='best')

	# color y axis labels
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