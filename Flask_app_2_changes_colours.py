# A very simple Flask Hello World app for you to get started with...

from flask import Flask

server = Flask(__name__)

@server.route('/dash/')
def hello_world():
    return 'Hello from Flask!'

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
#import numpy as np
# import time
from datetime import date, timedelta
###################
##### install dashdash_bootstrap_components
############# pip3 install dash-bootstrap-components


import dash_bootstrap_components as dbc



app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

##################################
### Data base

##################################
### Data base

df = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')

# print (df.head())
date_string = df['date']

DF_Date = df['date']
DF_Cases = df['total_cases']
DF_deaths = df['total_deaths']
DF_Continent = df['continent']
DF_country = df['location']
DF_people_vaccinated = df['people_vaccinated']

DF_total = pd.concat([DF_Date, DF_Continent, DF_country, DF_Cases, DF_deaths, DF_people_vaccinated], axis=1)

DF_total.columns = ['Date', 'Continent', 'Country', 'Total Infections', 'Total Deaths', 'Total Vaccinated']


##################################
#### Tabla resumen

#Today = date.today() ####Yestarday
#fecha2 = Today.strftime("%Y-%m-%d")

yesterday = date.today()-timedelta(days=1)
fecha2 = yesterday.strftime("%Y-%m-%d")
otro = df[df['date'] == fecha2]
Only_world2 = otro[otro['location'] == 'World']
Contagios = Only_world2['total_cases'].sum()
Total_deaths = Only_world2['total_deaths'].sum()
Vacunados = Only_world2['people_vaccinated'].sum()

total_res_wor = pd.DataFrame({'Infections': [Contagios],'Deaths': [Total_deaths], 'Vaccinated':[Vacunados] ,'Date':[fecha2]})

##################################
#### contagio fecha

Wd = df[df['location'] == 'World']

##################################
#### Mapa Contagios

otro2 = df[df['date'] == fecha2]
With_world = otro2[otro2['location'] != 'World']
actual = With_world[With_world['location'] != 'International'] 
actual = actual[actual['location'] != 'Europe']
actual = actual[actual['location'] != 'North America']
actual = actual[actual['location'] != 'Asia']
actual = actual[actual['location'] != 'South America']
actual = actual[actual['location'] != 'Africa']
actual = actual[actual['location'] != 'European Union']  
actual = actual[actual['location'] != 'South Africa']
actual = actual[actual['location'] != 'Oceania']  
actual = actual[actual['location'] != 'High income']  
actual = actual[actual['location'] != 'Upper middle income']  
actual = actual[actual['location'] != 'Lower middle income']  

#and 'North America' and 'Asia' and 'South America' and 'Africa'


#preview_actual = df.pivot_table(index = df['location']).reset_index()
##preview_actual = df.pivot_table(index = df['location'],aggfunc='max').reset_index()
#With_world = preview_actual[preview_actual['location'] != 'World']
#actual = With_world[With_world['location'] != 'International']

##################################
#### For cases and deaths select

Wd_cases = Wd['total_cases']
Wd_deaths = Wd['total_deaths']
Wd_people_vaccinated = Wd['people_vaccinated']
Wd_date = Wd['date']

date_cases_deaths = pd.concat([Wd_cases, Wd_deaths, Wd_people_vaccinated], axis=1)

date_cases_deaths.columns = ['Total Infections', 'Total Deaths', 'Total Vaccinated']

features = date_cases_deaths.columns


##################################
#### For map select

iso = actual['iso_code']
Map_total_cases = actual['total_cases']
Map_total_deaths = actual['total_deaths']
Map_people_vaccinated  = actual['people_vaccinated']
Pais = actual['location']

map_cases_deaths = pd.concat([iso, Map_total_cases, Map_total_deaths, Map_people_vaccinated, Pais], axis=1)

map_cases_deaths.columns = ['iso_code', 'Total Infections', 'Total Deaths', 'Total Vaccinated', 'Country']


##################################
#### For country select

Country_total_cases = actual['total_cases']
Country_total_deaths = actual['total_deaths']
Country_total_people_vaccinated = actual['people_vaccinated']
Pais = actual['location']

Country_total_cases_deaths = pd.concat([Country_total_cases, Country_total_deaths, Country_total_people_vaccinated, Pais], axis=1)

Country_total_cases_deaths.columns = ['Total Infections', 'Total Deaths', 'Total Vaccinated', 'Country']

##################################
#### For continent select

Continent_total_cases = actual['total_cases']
Continent_total_deaths = actual['total_deaths']
Continent_total_people_vaccinated = actual['people_vaccinated']
Continente = actual['continent']

Continent_total_cases_deaths = pd.concat([Continent_total_cases, Continent_total_deaths, Continent_total_people_vaccinated, Continente], axis=1)

Continent_total_cases_deaths.columns = ['Total Infections', 'Total Deaths', 'Total Vaccinated', 'Continent']


##################################
#### for table

# Table_total_cases = actual['total_cases']
# Table_total_deaths = actual['total_deaths']

table1 = pd.concat([Pais, Continente, Country_total_cases, Country_total_deaths, Country_total_people_vaccinated], axis=1)

table1.columns = ['Country', 'Continent','Total Infections', 'Total Deaths', 'Total Vaccinated']

##################################
#### app layout

colors = {
    'background': '#5A5766',
    #'text': '#FFFFFF'
}


app.layout = html.Div(style={'display':'block',
                              'background-color':'#48435C',
                              'margin-left':'auto',
                              'margin-right':'auto',
                              'text-align':'center',
                              'width': '95%',
                              'color':'white',
                              'border': '1px solid #000'}, children = [
                    html.H1('Covid analysis', style = {'background-color':'#5A5766', 'color':'white'}),
                    html.Br(),
                    html.Div([
                        html.H2('World overview', style = {'background-color':'#5A5766'}),
                        html.Br(),

                        dbc.CardDeck(
                                [
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("Infections", className="card-title"),
                                                html.P("{:,.0f}".format(total_res_wor['Infections'][0]),
                                                    className="card-text"
                                                )
                                            ]
                                        ),style = {'background-color':'#5A5766'},
                                    ),
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("Deaths", className="card-title"),
                                                html.P("{:,.0f}".format(total_res_wor['Deaths'][0]),
                                                    className="card-text"
                                                )
                                            ]
                                        ), style = {'background-color':'#5A5766'},
                                    ),
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("Vaccinated", className="card-title"),
                                                html.P("{:,.0f}".format(total_res_wor['Vaccinated'][0]),
                                                    className="card-text"
                                                )
                                            ]
                                        ), style = {'background-color':'#5A5766'},
                                    ),
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H5("Date report", className="card-title"),
                                                html.P("{}".format(total_res_wor['Date'][0]),
                                                    className="card-text"
                                                )
                                            ]
                                        ), style = {'background-color':'#5A5766'},
                                    ),
                                ]
                            )

                     ]),

                    ############
                    ## Contagios
                    html.Br(),
                    html.H2('Dashboard', style = {'background-color':'#5A5766'}),
                    html.P('Select Infections, Deaths or Vaccinated'),
                    html.Div([
                        dcc.Dropdown(id = 'yaxis',
                                    className='btn-sm m-0 p-0 pl-0 pr-0',
                                    options = [{'label': i, 'value': i} for i in features],
                                    value = 'Total Infections' ,style = {'background-color':'#F6F6F6', 'color': 'black'}
                                     )
                    ]),

                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                            dcc.Graph(id = 'date-graphic')
                                ), className="col-12 col-sm-6 col-lg-5"),
                                html.Br(),
                                dbc.Col(html.Div(
                                            dcc.Graph(id = 'map-graphic')
                                ), className="col-12 col-sm-6 col-lg-7"),
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                            dcc.Graph(id = 'country-graphic', style = {'background-color':'#5A5766', 'color': 'white'} )
                                ), className="col-12 col-sm-12 col-lg-12"),
                                html.Br(),
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                            dcc.Graph( id = 'continent-graphic', style = {'background-color':'#5A5766', 'color': 'white'} )
                                ), className="col-12 col-sm-6 col-lg-6"),
                                html.Br(),
                                dbc.Col(html.Div(
                                            dash_table.DataTable(
                                                    id='table',
                                                    columns=[{"name": i, "id": i, 'deletable': True} for i in sorted (table1.columns)],
                                                    data=table1.to_dict('records'),
                                                        page_current=0,
                                                        page_size=12,
                                                        page_action='custom',
                                                        sort_action='custom',
                                                        sort_mode='single',
                                                        sort_by=[],
                                                        style_table={'overflowY': 'auto'},
                                                        style_cell={'minWidth': 80, 'maxWidth': 80, 'width': 80, 'textAlign': 'center', 'color': 'black', #'backgroundColor': '#5A5766',
                                                                    }
                                                )

                                ), className="col-12 col-sm-6 col-lg-6"),
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                )),
                                html.Br(),
                            ]
                        ),
                        html.P('Select contry and infections or deaths'),
                        html.Div([
                        dcc.Dropdown(id = 'df_country',
                            options = [{'label': i, 'value': i} for i in DF_total.Country.unique()],
                            multi = True,
                            value = ['Colombia', 'Peru', 'Ecuador', 'Mexico', 'Argentina'],
                            style = {'background-color':'#F6F6F6', 'color': 'black'}
                            )
                        ]),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                            dcc.Graph(id = 'date-graphic-country', style = {'background-color':'#5A5766', 'color': 'white'} )
                                ), className="col-12 col-sm-12 col-lg-12"),
                                html.Br(),
                            ]
                        ),
                        html.Br(),

                        html.H2('Source', style = {'background-color':'#5A5766', 'color':'white'}),
                        html.Br(),
                        html.P('Information take from: ', style = {'text-align': 'center'}),
                        html.A("Our World In Data", href="https://ourworldindata.org", target="_blank", className="alert-link", style = {'color': 'white'}),
                        html.Br(),
                        html.Br(),
                        html.H3('Designed by: ', style = {'background-color':'#5A5766', 'color':'white'}),
                        html.Br(),
                        html.A("Andrés Triana", href="https://andresmtr.github.io/Andres_Triana_HV/", target="_blank", className="alert-link", style = {'color': 'white'}),
                        html.Br(),
                        html.Br(),


            ]

)


#########################
###### Mundo

@app.callback(Output('date-graphic', 'figure'),
                    [Input('yaxis', 'value')])
def upgrade_graph(yaxis_name):
    return {
        'data': [go.Scatter(x = Wd['date'],
                            y = date_cases_deaths[yaxis_name],
                            mode = 'lines',
                            line_color='rgb(231,107,243)',
                            marker = {'size':15,
                                     'opacity':0.5,
                                     'line':{'width':0.5, 'color':'white'}}
                                     ),
                ]


    ,'layout': go.Layout(title= yaxis_name+' by date',
                        xaxis = {'title': 'Date'},
                        yaxis = {'title': yaxis_name},
                        hovermode = 'closest',
                        #plot_bgcolor  = '#5A5766',
                        #paper_bgcolor  = '#5A5766',
                        #font_color = '#FFFFFF'
                        ),
            }



@app.callback(Output('map-graphic', 'figure'),
                    [Input('yaxis', 'value')])
def upgrade_map(yaxis_name_map):
    data = dict (type = 'choropleth',
                 locations = map_cases_deaths['iso_code'],
                 z = map_cases_deaths[yaxis_name_map],
                 text = map_cases_deaths['Country'],
                 colorscale="viridis",
                 colorbar = {'title': 'Infections and Deaths'} )

    layout = go.Layout(dict (geo = dict (showframe = False, projection = {'type':'mercator'}, #bgcolor = '#5A5766'
                                         ),
                         title='Map state by country',
                         hovermode = 'closest',
                         #plot_bgcolor  = '#5A5766',
                         #paper_bgcolor  = '#5A5766',
                         #font_color = '#FFFFFF'
                         ))

    return {"data": [data], "layout": layout}



@app.callback(Output('country-graphic', 'figure'),
                    [Input('yaxis', 'value')])
def upgrade_country(yaxis_name_country):
    if yaxis_name_country == 'Total Infections':
        Data_bar = Country_total_cases_deaths.sort_values('Total Infections',ascending=False).head(20)
    elif yaxis_name_country == 'Total Deaths':
        Data_bar = Country_total_cases_deaths.sort_values('Total Deaths',ascending=False).head(20)
    else:
        Data_bar = Country_total_cases_deaths.sort_values('Total Vaccinated',ascending=False).head(20)
        

    trace1 = go.Bar(x=Data_bar['Country'], y=Data_bar[yaxis_name_country])

    return {
        'data': [trace1]
    ,'layout': go.Layout(title= yaxis_name_country+' - first 20 countries',
                        xaxis = {'title': 'Country'},
                        yaxis = {'title': yaxis_name_country},
                        hovermode = 'closest',
                        #plot_bgcolor  = '#5A5766',
                        #paper_bgcolor  = '#5A5766',
                        #font_color = '#FFFFFF'
                        ),
            }


@app.callback(Output('continent-graphic', 'figure'),
                    [Input('yaxis', 'value')])
def upgrade_continent(yaxis_name_continent):
    return {
        'data': [go.Pie(labels = Continent_total_cases_deaths['Continent'],
                            values = Continent_total_cases_deaths[yaxis_name_continent],
                            hoverinfo='label+percent', textinfo='label+value+percent', textfont_size=10 ),

                ]


    ,'layout': go.Layout(title= yaxis_name_continent+' by Continent',
                        #plot_bgcolor  = '#5A5766',
                        #paper_bgcolor  = '#5A5766',
                        #font_color = '#FFFFFF'
                        ),
            }

@app.callback(
    Output('table', 'data'),
    [Input('table', "page_current"),
     Input('table', "page_size"),
     Input('table', 'sort_by')])
def update_table(page_current, page_size, sort_by):
    if len(sort_by):
        dff = table1.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = table1

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')


#########################
###### paises


@app.callback(Output('date-graphic-country', 'figure'),
                    [Input('df_country', 'value'),
                     Input('yaxis', 'value')])
def date_graph_country(country_values, yaxis_date_estate):
    dff = DF_total.loc[DF_total['Country'].isin(country_values)]
    return {
        'data': [go.Scatter(x=dff[dff['Country'] == Country]['Date'],
                            y=dff[dff['Country'] == Country][yaxis_date_estate],
                            name=Country,
                            # mode = 'Pais',
                            marker = {'size':15,
                                     'opacity':0.5,
                                     'line':{'width':0.5, 'color':'white'}}
                            )for Country in dff.Country.unique()],



    'layout': go.Layout(title= yaxis_date_estate+' by date',
                        xaxis = {'title': 'Date'},
                        yaxis = {'title': yaxis_date_estate},
                        hovermode = 'closest',
                        #plot_bgcolor  = '#5A5766',
                        #paper_bgcolor  = '#5A5766',
                        #font_color = '#FFFFFF'
                        ),
            }



if __name__ == "__main__":
    app.run_server()

