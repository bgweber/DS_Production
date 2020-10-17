import json
import pandas as pd
import tensorflow.keras as K


model = K.models.load_model("games.h5")


def lambda_handler(event, context):
    # read in the request body as the event dict
    if "body" in event:
        event = event["body"]
        event = json.loads(event) if event else {}
    
    if "G1" in event:
        new_row = {"G1": event["G1"], "G2": event["G2"],
                   "G3": event["G3"], "G4": event["G4"],
                   "G5": event["G5"], "G6": event["G6"], 
                   "G7": event["G7"], "G8": event["G8"], 
                   "G9": event["G9"], "G10": event["G10"]}
        
        new_x = pd.DataFrame.from_dict(data=new_row, 
                                       orient="index",
                                       dtype="float").T
        
        prediction = str(model.predict(new_x)[0][0])
        
        return {"body": "Prediction " + prediction}
    
    return {"body": "No parameters"}