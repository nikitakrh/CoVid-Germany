# CoViD-Germany
This is a little side-project I'm working on. Please never refer to this repository for information, I'm just working on my data visualization skills. For actual information, please visit [the webpage of RKI](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/Gesamt.html) (german institute to track infectious diseases).  
  
Overview of the current progress:
## Directories
### Data-Directory
This directory contains the current data on all kinds of information: hospitalizations, current cases, vaccination progress, etc. Data was collected on the 30th November 2021. The data collection will be automated in the future to contain the most up-to-date data.

### Util-Directory
This directory contains helper functions that are required for data processing and creating the plots for the dashboard.

## Scripts
### Data Collection
- handles the data
- automatically downloads data from official sites
- preprocesses the data for plotting
- saves only necessary data as csv for fast reading and plotting

Execute with:
`python collect_data.py`

### Dashboard App
- calls all plot functions to manage figures
- creates web app to be accessed via `http://127.0.0.1:8050/`

Execute with:  
`python dashboard_app.py`

### Hospitalizations
Plots:
- amount of cases that required hospitalization
	- in total and
	- by age
- hospitalization incidence by age

### Cases
Plots:
- amount of cases by age
- case incidence by age (averaged over 7 days, per 100.000 people)
- total amount of cases and the positive test rate

### Vaccine Effectiveness
Plots:
- Hospitalization rate over time (hospitalization per infection in %)
- Scatter of Case Incidence vs. vaccination rate for each federal state (+ linear regression line)
- Scatter of Hospitalization Incidence vs. vaccination rate for each federal state (+ linear regression line)
- Scatter of Hospitalization per Case Incidence vs. vaccination rate for each federal state (+ linear regression line)