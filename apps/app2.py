import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64
import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go

from app import app, df, countries
#Colors
colors = {
	'background': '#2A2E32',
	'bg_dark': '#1B1D20',
	#'bg_light': '#50565D',
	'bg_light':'#85909C',
	 'text': '#FFFFFF'
	 }
###################################################################################
######Pandas part##############
###################################################################################


#Get minimal value for axes bounds
def min_df(data):
    return min([min(data[y][~np.isnan(data[y])]) for y in list(data)[list(data).index('1960'):list(data).index('2017')+1] if len(data[y][~np.isnan(data[y])])>0])

#Get maximal value for axes bounds
def max_df(data):
    return max([max(data[y][~np.isnan(data[y])]) for y in list(data)[list(data).index('1960'):list(data).index('2017')+1] if len(data[y][~np.isnan(data[y])])>0])



###################################################################################
###################################################################################


layout = html.Div([
		#Überschrift 
		html.Div('Country vs. country',className = 'head_style'),
	html.Div([
		html.Div(['Indicator name'],className = 'd_exp_text'),
		html.Div([
		dcc.Dropdown(
				id = 'Type_exp',
  			  options=[{'label':x,'value':df[df['Indicator Name']==x]['Indicator Code'].unique()[0]} for x in df['Indicator Name'].unique()],
  			  #options = [{'label':'Electricity production from nuclear sources (% of total)','value':'EG.ELC.NUCL.ZS'}],
   		 		value='EG.ELC.NUCL.ZS'
		)],className = 'd_exp_1'
		),
		html.Div([
			dcc.Dropdown(
				id = 'country1',
				options = [{'label':x,'value':x} for x in df['Country Name'].unique()],
				value = 'China',
			)],className = 'd_country_1'),
		html.Div('vs.',className= 'text_country_1'),
		html.Div([
			dcc.Dropdown(
				id = 'country2',
				options = [{'label':x,'value':x} for x in df['Country Name'].unique()],
				value = 'United States',
			)],className = 'd_country_2'
		)],
		className = 'controls_country_1'),
		html.Div(children = '',
					id = 'scatter_plot',
					style = {
					'paddingTop': '10px',
    				'display': 'flex',
  					'justifyContent': 'center',
  					'alignItems': 'center'
  					}
				)
])


@app.callback(Output('scatter_plot','children'),
              [Input('Type_exp', 'value'),Input('country1', 'value'),Input('country2', 'value')])
def scatter_plot(type,country1,country2):
		temp1 = df[(df['Indicator Code']==type) & (df['Country Name']==country1)]
		temp2 = df[(df['Indicator Code']==type) & (df['Country Name']==country2)]
		x = [int(y) for y in list(df)[list(df).index('1960'):list(df).index('2017')+1]]
		y1 = [temp1[y][temp1.index[0]] for y in list(df)[list(df).index('1960'):list(df).index('2017')+1]]
		y2 = [temp2[y][temp2.index[0]] for y in list(df)[list(df).index('1960'):list(df).index('2017')+1]]
		return dcc.Graph(
					id = 'plot',
					figure = {
						'data': [ go.Scatter(
									x = x,
									y = y1, 
									mode = 'lines+markers', 
									marker=dict(color=colors['bg_light']),
									name = country1
											),
									go.Scatter(
									x = x,
									y = y2,
									mode = 'lines+markers',
									#marker=dict(color='#FF0000'),
									marker = dict(color='#E1161F'),
									name = country2
											)
								],
						'layout': go.Layout(
									plot_bgcolor = colors['background'],
									paper_bgcolor = colors['background'],
									font = {'color': colors['bg_light'] },
									#title = 'Random Data Scatterplot',
									xaxis = {'title': 'Year',
											'showgrid':False,
											'zeroline':False,
											'showline':True,
											'linecolor':colors['bg_dark']
											
											}, 
									yaxis = {'showgrid':False,
											'zeroline':False,
											'showline':True,
											'linecolor':colors['bg_dark']
											}, 
									#hovermode='closest'
									margin=dict(
     								   l=40,
       									r=40,
      									b=40,
        								t=40,
        								pad=0
       										 ),
        							height=450,
        							width= 900
											) 
							}
							)

