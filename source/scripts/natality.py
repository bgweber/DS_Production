
import json
import argparse
import joblib
import pandas as pd
import apache_beam as beam

from google.cloud import storage
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.io.gcp.datastore.v1new.types import Key
from apache_beam.io.gcp.datastore.v1new.types import Entity
from apache_beam.io.gcp.datastore.v1new.datastoreio import WriteToDatastore

class ApplyDoFn(beam.DoFn):

    def __init__(self):
        self.model = None
     
    def process(self, element):
        if self.model is None:
            bucket = storage.Client().get_bucket('dsp_model_store_00')
            blob = bucket.get_blob('natality/sklearn-linear')
            blob.download_to_filename('sklearn-linear')
            self.model = joblib.load('sklearn-linear')
        
        element = json.loads(element.decode('utf-8'))
        new_x = pd.DataFrame.from_dict(element, orient="index").T.fillna(0)   
        weight = self.model.predict(new_x.iloc[:, :8])[0]
        yield {'guid': element['guid'],
               'weight': weight,
               'time': str(element['time'])}
        
class CreateEntityDoFn(beam.DoFn):
    def process(self, element):
        key = Key(['natality-guid', element['guid']])
        entity = Entity(key)
        entity.set_properties({
            'weight': element['weight'],
            'time': element['time']
        })
        yield entity
        
# set up pipeline options
parser = argparse.ArgumentParser()
known_args, pipeline_args = parser.parse_known_args()
pipeline_options = PipelineOptions(pipeline_args)
project = pipeline_options.view_as(GoogleCloudOptions).project

# define the topics 
topic = "projects/{project}/topics/{topic}"
topic = topic.format(project=project, topic="natality")

# define the pipeline steps
p = beam.Pipeline(options=pipeline_options)
(p
 | 'Read PubSub' >> beam.io.ReadFromPubSub(topic=topic)
 | 'Apply Model' >> beam.ParDo(ApplyDoFn())
 | 'Create Entities' >> beam.ParDo(CreateEntityDoFn())
 | 'Save to Datastore' >> WriteToDatastore(project)
)

# run the pipeline
result = p.run()
result.wait_until_finish()
