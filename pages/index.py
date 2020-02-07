# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Predict the Intention of Online Shoppers

            A lot of businesses are online in the technology era, and it is understandable why people want to predict the intention of buying things online. This app gives you an accurate prediction of online shoppers' intentions. It will help you predict whether a user will end with or without shopping if you know some characteristics of them.
            
            *Note: This app is built for educational purposes and should not be used in business decisions.*  

            """
        ),
        dcc.Link(dbc.Button('Predict shopping intention', color='primary'), href='/predictions')
    ],
    md=4,
)

column2 = dbc.Col([html.Img(src='assets/homepage.jpg', className='img-fluid')
],
align='center'
)

layout = dbc.Row([column1, column2])
