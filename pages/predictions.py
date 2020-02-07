# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from joblib import load

# Imports from this application
from app import app

# Load pipeline
pipeline = load('assets/pipeline.joblib')
print('Pipeline loaded!')

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown('***Select values to make predictions!***'),

        dcc.Markdown('##### Page Value'),

        dcc.Slider(
            id='page_values',
            min=0,
            max=200,
            step=1,
            marks={
                0: '0',
                50: '50',
                100: '100',
                150: '150',
                200: '200',
            },
            value=0
        ),
        dcc.Markdown('',id='out_page_values'),

        dcc.Markdown("##### Month"),
        dcc.Dropdown(
            id='month',
            options=[
                {'label': 'February', 'value': 'Feb'},
                {'label': 'March', 'value': 'Mar'},
                {'label': 'May', 'value': 'May'},
                {'label': 'June', 'value': 'June'},
                {'label': 'July', 'value': 'Jul'},
                {'label': 'August', 'value': 'Aug'},
                {'label': 'September', 'value': 'Sep'},
                {'label': 'October', 'value': 'Oct'},
                {'label': 'November', 'value': 'Nov'},
                {'label': 'December', 'value': 'Dec'}
            ],
        value='MTL',
        className='mb-3'
        ),

        dcc.Markdown('##### Bounce Rate'),
        dcc.Markdown('*The percentage of visitors who enter the site and then leave without making any other requests*'),

        dcc.Slider(
            id='bounce_rates',
            min=0,
            max=1,
            step=0.01,
            marks={
                0: '0%',
                0.2: '20%',
                0.4: '40%',
                0.6: '60%',
                0.8: '80%',
                1: '100%'
            },
            value=0
        ),
        dcc.Markdown('',id='out_bounce_rates'),

        dcc.Markdown('##### Exit Rate'),
        dcc.Markdown('*The percentage to be the last in the session*'),

        dcc.Slider(
            id='exit_rates',
            min=0,
            max=1,
            step=0.01,
            marks={
                0: '0%',
                0.2: '20%',
                0.4: '40%',
                0.6: '60%',
                0.8: '80%',
                1: '100%'
            },
            value=0
        ),
        dcc.Markdown('',id='out_exit_rates'),
        
        
    ],
    md=4,
)

column2 = dbc.Col(
    [
        dcc.Markdown('', className='mb-5'),

        dcc.Markdown("##### Visits of the Administrative page"),
        dcc.Slider(
            id='administrative',
            min=0,
            max=25,
            step=1,
            marks={
                0: '0',
                5: '5',
                10: '10',
                15: '15',
                20: '20',
                25: '25'
            },
            value=0
        ),   
        dcc.Markdown('',id='out_administrative'),

        dcc.Markdown("##### Time spent on Administrative page (seconds)"),
        dcc.Slider(
            id='administrative_duration',
            min=0,
            max=2000,
            step=1,
            marks={
                0: '0',
                500: '500',
                1000: '1000',
                1500: '1500',
                2000: '2000',
            },
            value=0
        ),   
        dcc.Markdown('',id='out_administrative_duration'),

        dcc.Markdown("##### Visits of the Product Related page"),
        dcc.Slider(
            id='product_related',
            min=0,
            max=250,
            step=10,
            marks={
                0: '0',
                50: '50',
                100: '100',
                150: '150',
                200: '200',
                250: '250'
            },
            value=0
        ),   
        dcc.Markdown('',id='out_product_related'),

        dcc.Markdown("##### Time spent on the Product related page (seconds)"),
        dcc.Slider(
            id='product_related_duration',
            min=0,
            max=10000,
            step=100,
            marks={
                0: '0',
                2000: '2000',
                4000: '4000',
                6000: '6000',
                8000: '8000',
                10000: '10000'
            },
            value=0
        ),   
        dcc.Markdown('',id='out_product_related_duration'),
    ],
    md=4,
)

column3 = dbc.Col(
    [
        html.H2('Predicted Intention:', className='mb-3'), 
        html.Div(id='prediction-content', className='lead'),
        html.Div(id='image')
    ]
)

layout = dbc.Row([column1, column2, column3])

@app.callback(
    Output('prediction-content', 'children'),
    [Input('page_values', 'value'), Input('month', 'value'), Input('bounce_rates', 'value'),
    Input('exit_rates', 'value'), Input('administrative', 'value'), Input('administrative_duration', 'value'),
    Input('product_related', 'value'), Input('product_related_duration', 'value'),],
)
# Define predict function
def predict(page_values, month, bounce_rates, exit_rates, administrative, administrative_duration, product_related, product_related_duration):
    data = pd.DataFrame(
        columns=['PageValues', 'Month', 'BounceRates', 'ExitRates', 'Administrative', 'Administrative_Duration', 'ProductRelated', 'ProductRelated_Duration'], 
        data=[[page_values, month, bounce_rates, exit_rates, administrative, administrative_duration, product_related, product_related_duration]]
    )
    y_pred = pipeline.predict(data)[0]
    y_pred_proba = pipeline.predict_proba(data)[:,y_pred]
    probability = y_pred_proba*100
    if y_pred==1:
      result = 'buy'
    else:
      result = 'not buy'
    return f'There is a probability of {probability[0]:.2f}% that the user will {result} an item'

# Show different images depending on the result
@app.callback(
    Output('image', 'children'),
    [Input('page_values', 'value'), Input('month', 'value'), Input('bounce_rates', 'value'),
    Input('exit_rates', 'value'), Input('administrative', 'value'), Input('administrative_duration', 'value'),
    Input('product_related', 'value'), Input('product_related_duration', 'value'),],
)
def predict(page_values, month, bounce_rates, exit_rates, administrative, administrative_duration, product_related, product_related_duration):
    data = pd.DataFrame(
        columns=['PageValues', 'Month', 'BounceRates', 'ExitRates', 'Administrative', 'Administrative_Duration', 'ProductRelated', 'ProductRelated_Duration'], 
        data=[[page_values, month, bounce_rates, exit_rates, administrative, administrative_duration, product_related, product_related_duration]]
    )
    y_pred = pipeline.predict(data)[0]
    y_pred_proba = pipeline.predict_proba(data)[:,y_pred]
    probability = y_pred_proba*100
    if y_pred==1:
        return html.Img(src='assets/yes.jpg', className='img-flud', style={'height': '400px'})
    else:
        return html.Img(src='assets/no.jpg', className='img-flud', style={'height': '400px'})

@app.callback(
    Output(component_id='out_page_values', component_property='children'),
    [Input(component_id='page_values', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)
@app.callback(
    Output(component_id='out_bounce_rates', component_property='children'),
    [Input(component_id='bounce_rates', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)
@app.callback(
    Output(component_id='out_exit_rates', component_property='children'),
    [Input(component_id='exit_rates', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)
@app.callback(
    Output(component_id='out_administrative', component_property='children'),
    [Input(component_id='administrative', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)
@app.callback(
    Output(component_id='out_administrative_duration', component_property='children'),
    [Input(component_id='administrative_duration', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)
@app.callback(
    Output(component_id='out_product_related', component_property='children'),
    [Input(component_id='product_related', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)
@app.callback(
    Output(component_id='out_product_related_duration', component_property='children'),
    [Input(component_id='product_related_duration', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

