
import json
import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io.gcp.bigquery_tools import parse_table_schema_from_json

query = """
    SELECT 
        year,
        plurality, 
        apgar_5min,
        mother_age, 
        father_age,    
        gestation_weeks, 
        ever_born,
        CASE WHEN mother_married = true THEN 1 
             ELSE 0
        END AS mother_married,
        weight_pounds AS weight,
        CURRENT_TIMESTAMP AS time,
        GENERATE_UUID() AS guid
    FROM
        `bigquery-public-data.samples.natality`
    LIMIT
        100
"""

class ApplyDoFn(beam.DoFn):

    def __init__(self):
        import joblib
        import pandas as pd
        from google.cloud import storage
        self._model = None
        self._storage = storage
        self._joblib = joblib
        self._pd = pd
     
    def process(self, element):
        if self._model is None:
            bucket = self._storage.Client().get_bucket('dsp_model_store_00')
            blob = bucket.get_blob('natality/sklearn-linear')
            blob.download_to_filename('sklearn-linear')
            self._model = self._joblib.load('sklearn-linear')
        
        new_x = self._pd.DataFrame.from_dict(element, orient="index").T.fillna(0)   
        weight = self._model.predict(new_x.iloc[:, :8])[0]
        return [{'guid': element['guid'],
                 'weight': weight,
                 'time': str(element['time'])}]

schema = parse_table_schema_from_json(json.dumps({
    'fields': [{'name': 'guid', 'type': 'STRING'},
               {'name': 'weight', 'type': 'FLOAT64'},
               {'name': 'time', 'type': 'STRING'}]
}))

# set up pipeline options
parser = argparse.ArgumentParser()
known_args, pipeline_args = parser.parse_known_args()
pipeline_options = PipelineOptions(pipeline_args)

# define the pipeline steps
p = beam.Pipeline(options=pipeline_options)
data = p | 'Read from BigQuery' >> beam.io.ReadFromBigQuery(
    query=query, 
    use_standard_sql=True
)
scored = data | 'Apply Model' >> beam.ParDo(ApplyDoFn())
scored | 'Save to BigQuery' >> beam.io.WriteToBigQuery(
    table='weight_preds',
    dataset='dsp_demo', 
    schema=schema,
    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
)

# run the pipeline
result = p.run()
result.wait_until_finish()
