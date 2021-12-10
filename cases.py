import plotly.express as px

# TODO: plot cases and hospitalizations by age for each agegroup

def plot_cases_by_age(cases, cases_incidence):

	fig1 = px.line(
		cases, x='Meldedatum', y='Gesamt', 
		title='Cases of CoViD', labels={'Meldedatum': 'Date', 'Gesamt': 'Cases'}
	)
			
	fig1.add_traces(
		list(px.area(
			cases,
			x='Meldedatum',
			y=['Fälle A00..04', 'Fälle A05..14', 'Fälle A15..34', 'Fälle A35..59', 'Fälle A60..79', 'Fälle A80+'],
		).select_traces())
	)

	fig2 = px.line(
		cases_incidence, 
		x='Meldedatum', 
		y=['Inzidenz A00..04', 'Inzidenz A05..14','Inzidenz A15..34', 'Inzidenz A35..59', 'Inzidenz A60..79', 'Inzidenz A80+'], 
		title='Case Incidence by Age',
		labels={'Meldedatum': 'Date', 'value': 'Case Incidence', 'variable': 'Agegroups'}
	)

	figs = [fig1, fig2]

	return figs

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