
import apache_beam as beam
import argparse
from apache_beam.options.pipeline_options import PipelineOptions

parser = argparse.ArgumentParser()
known_args, pipeline_args = parser.parse_known_args(None)
pipeline_options = PipelineOptions(pipeline_args)

class ApplyDoFn(beam.DoFn):
    def process(self, element):
        print(element)


query = """
select *
from `bigquery-public-data.samples.natality`
order by rand()
limit 100 
"""

# define the pipeline steps 
p = beam.Pipeline(options=pipeline_options)
data = p | 'Read from BigQuery' >> beam.io.Read(
       beam.io.BigQuerySource(query=query, use_standard_sql=True))
scored = data | 'Apply Model' >> beam.ParDo(ApplyDoFn())

# run the pipeline 
result = p.run()
result.wait_until_finish()

