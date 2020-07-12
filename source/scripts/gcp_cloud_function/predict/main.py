model = None

def predict(request):
    global model

    import flask
    import pandas as pd
    import tensorflow.keras as K
    from google.cloud import storage

    data = {"success": False}
    params = request.get_json()
    
    if "G1" in params:
        new_row = {"G1": params.get("G1"), "G2": params.get("G2"),
                   "G3": params.get("G3"), "G4": params.get("G4"),
                   "G5": params.get("G5"), "G6": params.get("G6"),
                   "G7": params.get("G7"), "G8": params.get("G8"),
                   "G9": params.get("G9"), "G10":params.get("G10")}
        
        new_x = pd.DataFrame.from_dict(data=new_row, 
                                       orient="index",
                                       dtype="float").T

        # download model if not cached
        if not model:
            # set up access to the GCS bucket
            bucket_name = "dsp_model_store_00"
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(bucket_name)

            # download and load the model
            blob = bucket.blob("serverless/keras/v1")
            blob.download_to_filename("/tmp/games.h5")
            model = K.models.load_model("/tmp/games.h5")

        data["response"] = str(model.predict(new_x)[0][0])
        data["success"] = True
        
    return flask.jsonify(data)