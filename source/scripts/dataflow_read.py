
import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

parser = argparse.ArgumentParser()
known_args, pipeline_args = parser.parse_known_args()
pipeline_options = PipelineOptions(pipeline_args)

query = """
    SELECT
        *
    FROM
        `bigquery-public-data.samples.natality`
    ORDER BY
        RAND()
    LIMIT
        5
"""

# define the pipeline steps
p = beam.Pipeline(options=pipeline_options)
data = p | 'Read from BigQuery' >> beam.io.Read(
    beam.io.BigQuerySource(query=query, use_standard_sql=True)
)
scored = data | 'Print' >> beam.Map(print)

# run the pipeline
result = p.run()
result.wait_until_finish()
