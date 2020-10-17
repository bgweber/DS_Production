model = None

def pred_fast(request):
    global model

    import flask
    import joblib
    import sklearn
    import pandas as pd
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

        if not model:
            # set up access to the GCS bucket
            bucket_name = "dsp_model_store_00"
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(bucket_name)

            # download and load the model
            blob = bucket.blob("serverless/logit/v1")
            blob.download_to_filename("/tmp/local_logit.pkl")
            model = joblib.load("/tmp/local_logit.pkl")

        data["response"] = str(model.predict_proba(new_x)[0][1])
        data["success"] = True
        
    return flask.jsonify(data)