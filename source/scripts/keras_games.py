
import pandas as pd
import mlflow
import mlflow.keras
import flask
import tensorflow as tf
import keras as k

def auc(y_true, y_pred):
    auc = tf.metrics.auc(y_true, y_pred)[1]
    k.backend.get_session().run(
                  tf.local_variables_initializer())
    return auc

global graph
graph = tf.get_default_graph()
model_path = "models/keras_games_v1"
model = mlflow.keras.load_model(model_path, custom_objects={'auc': auc})

app = flask.Flask(__name__)

@app.route("/", methods=["GET","POST"])
def predict():
    data = {"success": False}
    params = flask.request.args

    if "G1" in params.keys(): 
        new_row = { "G1": params.get("G1"), "G2": params.get("G2"), 
                    "G3": params.get("G3"), "G4": params.get("G4"), 
                    "G5": params.get("G5"), "G6": params.get("G6"), 
                    "G7": params.get("G7"), "G8": params.get("G8"), 
                    "G9": params.get("G9"), "G10": params.get("G10") }

        new_x = pd.DataFrame.from_dict(new_row, orient = "index").transpose()                

        with graph.as_default():        
            data["response"] = str(model.predict(new_x)[0][0])
            data["success"] = True

    return flask.jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

#model.evaluate(x, y, verbose = 0)


