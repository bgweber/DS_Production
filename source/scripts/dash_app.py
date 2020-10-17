import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import mlflow.sklearn

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Model UI'),
    html.P([
        html.Label('Game 1 '),
        dcc.Input(value='1', type='text', id='g1'),
    ]),
    html.Div([
        html.Label('Game 2 '),
        dcc.Input(value='0', type='text', id='g2'),
    ]),
    html.P([
        html.Label('Prediction '),
        dcc.Input(value='0', type='text', id='pred')
    ]),
])

model_path = "models/logit_games_v1"
model  = mlflow.sklearn.load_model(model_path)

@app.callback(
    Output(component_id='pred', component_property='value'),
    [Input(component_id='g1', component_property='value'),
     Input(component_id='g2', component_property='value')]
)
def update_prediction(game1, game2):

    new_row = {"G1": float(game1), 
               "G2": float(game2), 
               "G3": 0, "G4": 0, 
               "G5": 0, "G6": 0, 
               "G7": 0, "G8": 0, 
               "G9": 0, "G10": 0}

    new_x = pd.DataFrame.from_dict(data=new_row,
                                   orient="index",
                                   dtype="float").T
    
    return str(model.predict_proba(new_x)[0][1])    

if __name__ == '__main__':
    app.run_server(host='0.0.0.0')