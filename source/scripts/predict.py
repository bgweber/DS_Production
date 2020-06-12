# import pickle
import flask
import mlflow
import mlflow.sklearn
import pandas as pd

#from sklearn.linear_model import LogisticRegression


# model = pickle.load(open("logit.pkl", 'rb'))
model_path = "models/logit_games_v1"
model  = mlflow.sklearn.load_model(model_path)


app = flask.Flask(__name__)

@app.route("/", methods=["GET","POST"])
def predict():
    data = {"success": False}
    params = flask.request.args

    if "G1" in params.keys(): 
        new_row = {"G1": params.get("G1"), "G2": params.get("G2"), 
                   "G3": params.get("G3"), "G4": params.get("G4"), 
                   "G5": params.get("G5"), "G6": params.get("G6"), 
                   "G7": params.get("G7"), "G8": params.get("G8"), 
                   "G9": params.get("G9"), "G10":params.get("G10")}

        new_x = pd.DataFrame.from_dict(data=new_row, 
                                       orient="index", 
                                       dtype='int').T
        
        data["response"] = str(model.predict_proba(new_x)[0][1])
        data["success"] = True

    return flask.jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
