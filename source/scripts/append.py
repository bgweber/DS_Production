
import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText

# define a function for transforming the data 
class AppendDoFn(beam.DoFn):
    def process(self, element):
        yield element + " - Hello World!"
        
# set up pipeline parameters 
parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input',
                    default='gs://dataflow-samples/shakespeare/kinglear.txt')
parser.add_argument('--output', dest='output',
                    default='gs://dsp_model_store_00/shakespeare/kinglear.txt')
known_args, pipeline_args = parser.parse_known_args()
pipeline_options = PipelineOptions(pipeline_args)

# define the pipeline steps 
p = beam.Pipeline(options=pipeline_options)
lines = p | 'read' >> ReadFromText(known_args.input)
appended = lines | 'append' >> beam.ParDo(AppendDoFn())
appended | 'write' >> WriteToText(known_args.output)

# run the pipeline 
result = p.run()
result.wait_until_finish()
