import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import base64



from app import app, server
from apps import app1, app2

#Colors
colors = {
	'background': '#2A2E32',
	'bg_dark': '#1B1D20',
	'bg_light':'#85909C',
	 'text': '#FFFFFF'
}

#import images
def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())


#Layout of homescreen
app.layout = html.Div([
	#Create url...
    dcc.Location(id='url', refresh=False),
    #Create a menu button using an image
    #Put menubutton and menu in one div to have the menu below it
    html.Div([
		html.Img(src=encode_image('./images/menu-square-button.png'),
    				height = 15,
    				id='mb_img',
    				className = 'buttonstyle',
    				n_clicks = 0
    			),
		html.Div(id='menu-content',className='menustyle_off')],
	 	className = 'menu_button_position'
	    ),
	#Password part
	html.Div([
				html.Div('Login',style = {'text-align':'center','color':colors['bg_light'],'font-family':'sans-serif','paddingTop':'20px'}),
				html.Div(dcc.Input(
				id = 'username',
   				 placeholder='Enter username',
   				 type='text',
    			value=''
				),className = 'username'),
				html.Div(dcc.Input(
				id = 'password',
    			placeholder='Enter password',
    			type='text',
    			value=''
				),className = 'password')
			],id = 'password_div',className = 'password_div'
	),
	 #Insert the apps right here!
    html.Div('',id='page-content',
    className = 'appstyle',style={'display':'none'}
    )
],
	className= 'backgroundstyle'
)

#################################################################
#Callbacks
#################################################################

#Callback for password
@app.callback(Output('page-content', 'style'),
              [Input('username', 'value'),Input('password','value')])
def password(username,password):
	if (username == 'WDI_app') & (password == '001D73'):
		return {}
	else:
		return {'display':'none'}
		
#Callback for password
@app.callback(Output('password_div', 'style'),
              [Input('username', 'value'),Input('password','value')])
def password(username,password):
	if (username == 'WDI_app') & (password == '001D73'):
		return {'display':'none'}
	else:
		return {}

#Callback to switch between apps
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_apps(pathname):
	if pathname == '/':
		return app1.layout
	elif pathname == '/apps/app1':
		return app1.layout
	elif pathname == '/apps/app2':
		return app2.layout
	else:
		return app1.layout
        
#Callback for constructing menu
@app.callback(Output('menu-content', 'children'),
              [Input('mb_img', 'n_clicks')])
def display_menu(button):
    if button%2 != 0:
         return [
         		dcc.Link(
         			html.Div('Explore',id='menu1',className='active_menuitem')
         			,href='/apps/app1',style = {'display':'block','textDecoration':'none'}
         		),
         		dcc.Link(
         			html.Div('Country vs. country',id='menu2',className='inactive_menuitem')
         			,href='/apps/app2',style = {'display':'block','textDecoration':'none'}
         		)
         		]
    if button%2 == 0:
         return ''

#Callback for menu changes menustyle width    
@app.callback(Output('menu-content', 'className'),
              [Input('mb_img', 'n_clicks')])
def display_menu(button):
    if button%2 != 0:
         return 'menustyle_on'
    elif button%2 == 0:
         return 'menustyle_off'

#Callback for menubutton
@app.callback(Output('mb_img', 'src'),
              [Input('mb_img', 'n_clicks')])
def change_buttonstyle(button):
	if button%2 != 0:
		return encode_image('./images/menu-square-button_dark.png')
	elif button%2 == 0:
		return encode_image('./images/menu-square-button.png')
		
#Callback for menuitems
@app.callback(Output('menu1', 'className'),
              [Input('url', 'pathname'),Input('mb_img', 'n_clicks')])
def change_buttonstyle2(pathname,clicks):
	if clicks%2 !=0:
		if (pathname == '/apps/app1') or (pathname == '/'):
			return 'active_menuitem'
		else:
			return 'inactive_menuitem'
						
@app.callback(Output('menu2', 'className'),
              [Input('url', 'pathname'),Input('mb_img', 'n_clicks')])
def change_buttonstyle2(pathname,clicks):
	if clicks%2 !=0:
		if pathname == '/apps/app2':
			return 'active_menuitem'
		else:
			return 'inactive_menuitem'


if __name__ == '__main__':
    app.run_server(debug=True)