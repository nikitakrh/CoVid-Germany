# CoViD-Germany
This is a little side-project I'm working on. Please never refer to this repository for information, I'm just working on my data visualization skills. For actual information, please visit [the webpage of RKI](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/Gesamt.html) (german institute to track infectious diseases).  
  
Overview of the current progress:
## Directories
### Data-Directory
This directory contains the current data on all kinds of information: hospitalizations, current cases, vaccination progress, etc. Data was collected on the 30th November 2021. The data collection will be automated in the future to contain the most up-to-date data.

### Util-Directory
This directory contains helper functions that are required for data processing.

## Scripts
### Hospitalizations by age
This script plots:
- the amount of cases that required hospitalization
	- in total and
	- by age.
- the hospitalization incidence by age  

Execute with:  
  
`python hospitalizations_by_age.py`

### Cases by age
This script plots:
- the amount of cases
	- in total and
	- by age
- the case incidence (averaged over 7 days, per 100.000 people)
	- in total and
	- by age  

Execute with:  

`python cases_by_age.py`