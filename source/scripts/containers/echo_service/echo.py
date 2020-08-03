# load Flask 
import flask
app = flask.Flask(__name__)

# define a predict function as an endpoint 
@app.route("/predict", methods=["GET", "POST"])
def predict():
    data = {"success": False}
    
    # check for passed in parameters   
    params = flask.request.json
    if params is None:
        params = flask.request.args
    
    # if parameters are found, echo the msg parameter 
    if "msg" in params.keys(): 
        data["response"] = params.get("msg")
        data["success"] = True
        
    # return a response in json format 
    return flask.jsonify(data)
    
# start the flask app, allow remote connections
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
