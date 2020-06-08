
import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

model = pickle.load(open("logit.pkl", 'rb'))

# load Flask
import flask
app = flask.Flask(__name__)

# define a predict function as an endpoint
@app.route("/", methods=["GET"])
def predict():
    data = {"success": False}

    # get the request parameters
    params = flask.request.args

    # if parameters are found, echo the msg parameter
    if (params != None):
        new_row = { "G1": params.get("G1"), "G2": params.get("G2"), 
                    "G3": params.get("G3"), "G4": params.get("G4"), 
                    "G5": params.get("G5"), "G6": params.get("G6"), 
                    "G7": params.get("G7"), "G8": params.get("G8"), 
                    "G9": params.get("G9"), "G10": params.get("G10") }

        new_x = pd.DataFrame.from_dict(new_row, orient = "index").transpose()                
        data["response"] = str(model.predict_proba(new_x)[0][1])
        data["success"] = True

    # return a response in json format
    return flask.jsonify(data)

# start the flask app, allow remote connections
app.run(host='0.0.0.0')


