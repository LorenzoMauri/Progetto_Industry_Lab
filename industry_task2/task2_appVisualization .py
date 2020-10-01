import dash
import pandas as pd 
import numpy as np 
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output
import plotly.express as px
import plotly.graph_objects as go

colors = {'background_plot' : '#070707',
'background_paper':'#000000',
'font_color':'#061ef8'
}

####################################
### app initialization #############
####################################

app = dash.Dash(__name__,assets_external_path='assets/')

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        
        # x=[2],
        # y=[4.5]  #,marker=dict(color='LightSkyBlue',size=30 )
    ))


fig.update_layout(
    plot_bgcolor=colors['background_plot'],
    #paper_bgcolor=colors['background_paper'],
    font_color=colors['font_color'],
    margin=dict(l=0,r=0,b=0,t=0,pad=0),paper_bgcolor=colors["background_paper"]
)

fig.update_layout(showlegend=False)
fig.update_xaxes(title_text="Leakage Coefficient")
fig.update_yaxes(title_text="Outflow Pressure")
fig.update_layout(xaxis_range = [0,51],
        yaxis_range = [0,6],margin=dict(l=0,r=0,b=0,t=0,pad=0),
        paper_bgcolor=colors["background_paper"]
    )
fig.update_layout(
    plot_bgcolor=colors['background_plot'],
    #paper_bgcolor=colors['background_paper'],
    font_color=colors['font_color'],
    yaxis = dict(titlefont=dict(size=30)),
    xaxis = dict(titlefont=dict(size=30) )
)

#########################################
### title, dropdown menu, html ##########
#########################################

app.layout= html.Div(id = 'main_div',
    children=[html.H1("VERIFICA DEI LIMITI DI PORTATA PER TIPOLOGIA DI POMPA"),
html.H3("Select a Pump type"),
dcc.Dropdown(id = 'pump_types',
    options=[
        {'label': 'STD Pump', 'value': 'STD'},
        {'label': 'DAI Pump', 'value': 'DAI'}
    ],
    placeholder = 'STD or DAI type'
)  ,
html.H3("Select a value for Leakeage Coefficient"),
html.Div(id = 'leakage',children=[
    dcc.Input(id = 'leakege_coefficient',
    placeholder='0.0',type='number')]),
html.Br(),
html.H3("Select a value for Outflow Pressure"),
html.Br(),
dcc.Input(id = 'outline_pressure',placeholder='0.0',type='number'),


html.Div(id = 'outflow_text',children=[]),


####################################
######### plots ####################
####################################
html.Br(),
dcc.Graph(id = 'my_plot',figure =fig) ,
html.Br(),
html.Div(id = 'names',children = 
[html.H2('Lorenzo Mauri, Marco Distrutti, Antonio Pennacchia')])
 ])


####################################
######## callbacks #################
####################################

@app.callback(
    [Output(component_id = 'my_plot',component_property='figure'),
    Output(component_id = 'outflow_text',component_property='children')],
    [Input(component_id= 'pump_types' ,component_property='value'),
    Input(component_id= 'leakege_coefficient' ,component_property='value'),
    Input(component_id= 'outline_pressure' ,component_property='value')])

def update_graph(pump_type,leakege_coefficient,outline_pressure):    # callback function : an argument per Input 
    inf_a,sup_a,inf_p,sup_p = 0,0,0,0
   
    #############################################
    ######## limits feasible region #############
    #############################################

    if pump_type == "STD":
        inf_a=11
        sup_a=30
        inf_p=1.75
        sup_p=3
    else :
        inf_a=20
        sup_a=50
        inf_p=1.25
        sup_p=2.25
    
    fig=go.Figure()

    ##############################
    #### feasible region #########
    ##############################

    fig.add_trace(go.Scatter(x=[inf_a,inf_a,sup_a,sup_a,inf_a], y=[inf_p,sup_p,sup_p,inf_p,inf_p],
                    fill='toself', fillcolor='light gray',
                    #hoveron = 'fills', # select where hover is active
                    hoverinfo = 'x+y'))
    if (inf_a <= leakege_coefficient  <= sup_a) and (inf_p <= outline_pressure <= sup_p ): 
        point_color = 'green'
    else : point_color = 'red'
    
    ###############################
    ######## data point ###########
    ###############################
    
    fig.add_trace(go.Scatter(x=[leakege_coefficient], y=[outline_pressure],hoverinfo = 'x+y',
    marker=dict(size=30,color=point_color),opacity = 0.8))
    fig.update_layout(xaxis_range = [0,51],
        yaxis_range = [0,6],margin=dict(l=0,r=0,b=0,t=0,pad=0),
        paper_bgcolor=colors["background_paper"]
    )
    fig.update_layout(
    plot_bgcolor=colors['background_plot'],
    #paper_bgcolor=colors['background_paper'],
    font_color=colors['font_color']
)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title_text="Leakage Coefficient")
    fig.update_yaxes(title_text="Outflow Pressure")
    fig.update_layout(yaxis = dict(titlefont=dict(size=30)),
    xaxis = dict(titlefont=dict(size=30)))
    portata = 108.36 - (leakege_coefficient*outline_pressure)
    portata_text = f"Output Flow : {portata} l/h"
    return (fig,portata_text)       # return 2 outputs as stated before in callback



####################################
######### running server ###########
####################################

if __name__ == '__main__':
         app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)


         