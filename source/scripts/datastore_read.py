
import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.io.gcp.datastore.v1new.datastoreio import ReadFromDatastore
from apache_beam.io.gcp.datastore.v1new.types import Query

parser = argparse.ArgumentParser()
known_args, pipeline_args = parser.parse_known_args(None)
pipeline_options = PipelineOptions(pipeline_args)
project = pipeline_options.view_as(GoogleCloudOptions).project

# define the pipeline steps
p = beam.Pipeline(options=pipeline_options)

data = p | 'Read from Datastore' >> ReadFromDatastore(
    query=Query('natality-guid', project, limit=5)
)
scored = data | 'Print' >> beam.Map(print)

# run the pipeline
result = p.run()
result.wait_until_finish()
