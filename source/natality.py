import apache_beam as beam
import argparse
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.bigquery import parse_table_schema_from_json
import json

class ApplyDoFn(beam.DoFn):

    def __init__(self):
        self._model = None
        from google.cloud import storage
        import pandas as pd
        import pickle as pkl
        import json as js
        self._storage = storage
        self._pkl = pkl
        self._pd = pd
        self._json = js
     
    def process(self, element):
        if self._model is None:
            bucket = self._storage.Client().get_bucket(
                                                 'dsp_model_store')
            blob = bucket.get_blob('natality/sklearn-linear')
            self._model =self._pkl.loads(blob.download_as_string())
        
        element = self._json.loads(element.decode('utf-8'))
        new_x = self._pd.DataFrame.from_dict(element, 
                            orient = "index").transpose().fillna(0)   
        weight = self._model.predict(new_x.iloc[:,1:8])[0]
        print(str(weight))
        return [ { 'guid': element['guid'], 'weight': weight, 
                                   'time': str(element['time']) } ]
             
class PublishDoFn(beam.DoFn):
    
    def __init__(self):
        from google.cloud import datastore       
        self._ds = datastore
    
    def process(self, element):
        client = self._ds.Client()
        key = client.key('natality-guid', element['guid'])
        entity = self._ds.Entity(key)
        entity['weight'] = element['weight']         
        entity['time'] = element['time']
        print("publish")
        print(entity)
        client.put(entity)
            
# set up pipeline parameters 
parser = argparse.ArgumentParser()
known_args, pipeline_args = parser.parse_known_args(None)
pipeline_options = PipelineOptions(pipeline_args)

# define the topics 
topic = "projects/{project}/topics/{topic}"
topic = topic.format(project = "gameanalytics-199018", topic = "natality")

schema = parse_table_schema_from_json(json.dumps({'fields':
            [ { 'name': 'guid', 'type': 'STRING'},
              { 'name': 'weight', 'type': 'FLOAT64'},
              { 'name': 'time', 'type': 'STRING'} ]}))

# define the pipeline steps 
p = beam.Pipeline(options=pipeline_options)
lines = p | 'Read PubSub' >> beam.io.ReadFromPubSub(topic=topic)
scored = lines | 'apply' >> beam.ParDo(ApplyDoFn())
scored | 'Create entities' >> beam.ParDo(PublishDoFn())

# run the pipeline 
result = p.run()
result.wait_until_finish()

