# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
            ### Overview

            This project uses the [Online Shoppers Purchasing Intention 
            Dataset](https://archive.ics.uci.edu/ml/datasets/Online+Shoppers+Purchasing+Intention+Dataset#) from UCI. According to the Dataset 
            description, it was formed so that each session would belong to a different user in a 1-year period to avoid any 
            tendency to a specific campaign, special day, user profile, or period. The dataset consists of 10 numerical and 8 categorical 
            attributes.

            The main task of the project is to predict the users' intention of purchase or the attribute `Revenue`, which is a
            boolean variable describing either the user made a purchase or not. 
            The majority class of the database is the False value; this negative class appearing with a frequency of 84.5%.
            Only 15.5% of users ended with an online purchase. 
            """
        ),

         html.Img(src='assets/baseline.png', 
                 className='img-fluid', 
                 style={'display': 'block', 'width' : '20%'}),
        
        dcc.Markdown(
            """
            For this project, it is essential to correctly predict the positive class, whose frequency is smaller than the negative class. 
            Because the classes are imbalanced, the accuracy is not the best evaluation metric, so I used the Area Under the Receiver 
            Operating Characteristic Curve (ROC AUC) as an evaluation metric.

            ### Data Processing

            The dataset had the following problems to be solved:

            1. 125 rows (1.0%) were duplicate; 

            2. The numerical variables contained outliers;

            3. Some categorical variables with numeric values were integer, and we need them strings. 

            After cleaning and wrangling data, the dataset was split into train, validate, and test datasets using the random split. I tried
            more models before deciding on which to use.

            ### First model: Logistic Regression
            First, I tried a linear model for classification, the logistic regression, using `LogisticRegressionCV()`. The ROC AUC score for
            this model was 0.8827, and the most important features were highlighted: Page values, Exit rates, Month, number of visits on Product
            related page, and the time spent on Product related page.
            """
        ),

        html.Img(src='assets/logistic.png', className='img-fluid', 
                 style={'display': 'block', 'width' : '60%'}),
        
        dcc.Markdown(
            """

            ### Random Forest Classifier

            For the second model, I used `RandomForestClassifier` with `n_estimators=100`, and I received a validation ROC AUC score equals
            to 0.9179.

            To improve this model, I optimized 3+ hyperparameters by trying 10+ candidates. 
            """
        ),

        html.Img(src='assets/random_forest.png', className='img-fluid', 
                 style={'display': 'block', 'width' : '40%'}),
        
        dcc.Markdown("Using the best parameters of the model, I increased the validation ROC AUC score up to 0.9263."),

        html.Img(src='assets/roc.png', className='img-fluid', 
                 style={'display': 'block', 'width' : '40%'}),

        dcc.Markdown(
            """
            I tried to use xgboost, but it didn't improve the model performance, so I decided to choose the RandomForestClassifier model
            with the best parameters: `max_depth=5`, `max_features=0.7164353684966558`, `n_estimators=460`. The most important features 
            highlighted by this model are the Page values, Bounce rates, Month, Exit rates, the number of visits on the product related page
            and on administrative page, as well as the time spent on these pages.
            """
        ),

        html.Img(src='assets/top10.png', className='img-fluid', 
                 style={'display': 'block', 'width' : '60%'}),

        dcc.Markdown("Before deciding on the most important features, I used the `eli5` library to find the permutation importances."),

        html.Img(src='assets/permutation.png', className='img-fluid', 
                 style={'display': 'block', 'width' : '30%'}),
        
        dcc.Markdown(
            """
            Finally, I decided to use in the model only the most important features, because it is easier to interpret and to make 
            predictions by giving different values as input for fewer variables.
            """
        ),

        html.Img(src='assets/test_score.png', className='img-fluid', 
                 style={'display': 'block', 'width' : '80%'}),
        
        dcc.Markdown(
            """
            Even if the validation score is lower than the score using all 18 features, the test score is equal to 0.9309, giving me enough
            confidence to use this model to predict the intention of online shoppers. The value of the page is the most important feature
            in the model. Please find below the partial dependence plot for it.
            """
        ),

        html.Img(src='assets/pdp_page_values.png', className='img-fluid', 
                 style={'display': 'block', 'width' : '60%'}),

        dcc.Markdown(
            """
            ### Summary
            * This app predicts the intention of online shoppers
            * The best model is Random Forest with the following arguments: 
            `RandomForestClassifier(max_depth=5, max_features=0.7164353684966558, n_estimators=460, random_state=42, n_jobs=-1)`
            * The test score of 0.93 beats the baseline score

            ### References:
            Sakar, C.O., Polat, S.O., Katircioglu, M. et al. Neural Comput & Applic (2019) 31: 6893. https://doi.org/10.1007/s00521-018-3523-0
            """
        ),
    ],
)



layout = dbc.Row([column1])