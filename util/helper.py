import os
import requests
import pandas as pd

util_dir = os.path.dirname(__file__)
data_dir = os.path.join(os.path.join(util_dir, os.pardir), 'data/')

def style_fig(fig, colors):
	fig.update_layout(
		plot_bgcolor=colors['tile'],
		paper_bgcolor=colors['background'],
		font_color=colors['text']
	)
	return fig


# TODO: file download + dataframe in own method
def download_data(url, sheet=None, header=None, index_col=None, sep=',', nrows=None):
	r = requests.get(url, allow_redirects=True)

	if('.xlsx' in url):
		with open(data_dir + 'temp.xlsx', 'wb') as f:
			f.write(r.content)
			try:
				df = pd.read_excel(data_dir + 'temp.xlsx', sheet_name=sheet, header=header, index_col=index_col, nrows=nrows, engine='openpyxl')
				os.remove(data_dir + 'temp.xlsx')
			except:
				df = pd.read_excel(data_dir + 'temp.xlsx', sheet_name=sheet, header=header, index_col=index_col, nrows=nrows, engine='xlrd')
	else:
		with open(data_dir + 'temp.csv', 'wb') as f:
			f.write(r.content)
			df = pd.read_csv(data_dir + 'temp.csv', sep=sep, header=header)
		os.remove(data_dir + 'temp.csv')

	return df