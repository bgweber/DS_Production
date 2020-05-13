import apache_beam as beam
import argparse
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io.gcp.bigquery import parse_table_schema_from_json
import json

query = """
    SELECT year, plurality, apgar_5min, 
    mother_age, father_age,    
       gestation_weeks, ever_born
       ,case when mother_married = true 
          then 1 else 0 end as mother_married
      ,weight_pounds as weight
      ,current_timestamp as time
      ,GENERATE_UUID() as guid
    FROM `bigquery-public-data.samples.natality` 
    limit 100    
"""

class ApplyDoFn(beam.DoFn):

    def __init__(self):
        self._model = None
        from google.cloud import storage
        import pandas as pd
        import pickle as pkl
        self._storage = storage
        self._pkl = pkl
        self._pd = pd
     
    def process(self, element):
        if self._model is None:
            bucket = self._storage.Client().get_bucket('dsp_model_store')
            blob = bucket.get_blob('natality/sklearn-linear')
            self._model = self._pkl.loads(blob.download_as_string())
        
        new_x = self._pd.DataFrame.from_dict(element, orient = "index").transpose().fillna(0)   
        weight = self._model.predict(new_x.iloc[:,1:8])[0]
        return [ { 'guid': element['guid'], 'weight': weight, 'time': str(element['time']) } ]

schema = parse_table_schema_from_json(json.dumps({'fields':
            [ { 'name': 'guid', 'type': 'STRING'},
              { 'name': 'weight', 'type': 'FLOAT64'},
              { 'name': 'time', 'type': 'STRING'} ]}))

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
        client.put(entity)

parser = argparse.ArgumentParser()
known_args, pipeline_args = parser.parse_known_args(None)
pipeline_options = PipelineOptions(pipeline_args)

# define the pipeline steps
p = beam.Pipeline(options=pipeline_options)
data = p | 'Read from BigQuery' >> beam.io.Read(
       beam.io.BigQuerySource(query=query, use_standard_sql=True))
scored = data | 'Apply Model' >> beam.ParDo(ApplyDoFn())
scored | 'Save to BigQuery' >> beam.io.Write(beam.io.BigQuerySink(
                'weight_preds', 'dsp_demo', schema = schema,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))

scored | 'Create entities' >> beam.ParDo(PublishDoFn())

# run the pipeline
result = p.run()
result.wait_until_finish()

