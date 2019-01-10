import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64
import pandas as pd
import numpy as np
import plotly.plotly as py


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

#Need country code as index and only the values in the first column
indcode = 'EN.ATM.CO2E.KT'
dicts_CO2 = df[df['Indicator Code']==indcode].set_index('Country Code').copy()
year = '2014'
zmin = min_df(dicts_CO2)
zmax = max_df(dicts_CO2)


###################################################################################
###################################################################################

#Function that constructs choropleth by inserting data and year
def graph_fig(wdata,year,zzmin,zzmax):
    g_data = [ dict(
        type = 'choropleth',
        locations = wdata[year].index,
        z = wdata[year].values,
        text = wdata['Country Name'].values,
        colorscale = [[0,'#5A636C'],[1,'rgb(255,0,0)']],
        zmax = zzmax,
        zmin = zzmin,
        zauto = False,
        autocolorscale = False,
        #opacity = 0.1,
        reversescale = False,
        marker = dict(
            line = dict(
                #color = 'rgb(180,180,180)',
                color = '#1B1D20',
                #color = 'white',
                width = 0.5
            )),
        #tickcolor = '#000',
        colorbar = dict(
            autotick = False,
            tickfont = {'color':colors['bg_light']}
            )
      )]
      
    g_layout = dict(
        geo = dict(
            showframe = False,
            paper_bgcolor= 'black',
            map_bgcolor='black',
            showcoastlines = True,
            projection = dict(
                type = 'Mercator'
            ),
            showocean = False,
            #oceancolor= "rgb(17,122,152)",
            showland = True,
            landcolor = colors['background'],
            bgcolor = colors['background'],
        ),
        paper_bgcolor= colors['background'],
        autosize = False,
        margin=dict(
        l=0,
        r=0,
        b=0,
        t=20,
        pad=0
        ),
        height=450,
        width= 900
    )
    return dict(data=g_data,layout=g_layout)


layout = html.Div([
		#Überschrift 
		html.Div('Explore',className = 'head_style'),
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
		html.Div(['Year'],className = 's_co2_1_text'),
		html.Div(['Axis range'],className = 's_co2_2_text'),
		html.Div([
		dcc.Slider(
			id = 'year_exp',
 		   min=1960,
 		   max=2017,
 		   step=1,
 		   marks = {},
 		   value=2014,
 		   updatemode='drag'
		)
		],
		className = 'slider_left'
		),
		html.Div(className = 'slider_right',
				id = 'axes_exp')
		],className = 'controls_co2_1'),
		#Somehow necessary to avoid graph moving to the left
		html.Div('',id='test',style={'width':'100%','border':'0px black solid','paddingTop':'15px'}),
		html.Div(
			[dcc.Graph(
				id='world_exp', 
				figure = graph_fig(dicts_CO2,'2014',min_df(dicts_CO2),max_df(dicts_CO2)),
					)]
				,style = {
				'paddingTop': '0px',
    			'display': 'flex',
  				'justifyContent': 'center',
  				'alignItems': 'center'
  				}
				)
])

#################################################################################
#Slider -----> Slider
#################################################################################
#Display slider value 1
@app.callback(Output('year_exp', 'marks'),
              [Input('year_exp', 'value')])
def display_slidervalue1(value):
	return 	{value:{'label':'{}'.format(value),'style': {'color': 'white','font-family':'sans-serif','font-size':'13px'}}}
		

	
##################################################################################
#Dropdown Type -----> RangeSlider
##################################################################################
@app.callback(Output('axes_exp','children'),
              [Input('Type_exp','value')])
def range_slider(value):
	temp_df = df[df['Indicator Code']==value].set_index('Country Code').copy()
	min_temp =  min_df(temp_df)
	if (min_temp <0.0001) & (min_temp >0):
		min_temp = 0
	max_temp =  max_df(temp_df)
	return dcc.RangeSlider(id = 'axes_1_exp',
				min = min_temp,
				max = max_temp,
				step = (max_temp-min_temp)/100,
				value = [min_temp,max_temp],
				updatemode='drag'
				)

##################################################################################
#Slider range -----> Slider range
##################################################################################
@app.callback(Output('axes_1_exp', 'marks'),
              [Input('axes_1_exp', 'value')])
def display_slidervalue2(value):
	return 	{
			value[0]:{'label':'{:.2e}'.format(value[0]),'style': {'color': 'white','font-family':'sans-serif','font-size':'13px'}},
			value[1]:{'label':'{:.2e}'.format(value[1]),'style': {'color': 'white','font-family':'sans-serif','font-size':'13px'}}
			}

##################################################################################
#type, year, axes_1 -----> world figure
##################################################################################
@app.callback(Output('world_exp', 'figure'),
              [Input('year_exp', 'value'),Input('Type_exp','value'),Input('axes_1_exp', 'value')])
def change_worldplot(year,type,value):
	temp_df = df[df['Indicator Code']==type].set_index('Country Code').copy()
	return 	graph_fig(temp_df,'{}'.format(year),value[0],value[1])

