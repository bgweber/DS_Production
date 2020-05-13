import apache_beam as beam
import argparse
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText

# define a function for transforming the data 
class AppendDoFn(beam.DoFn):
    def process(self, element):
        return "Hello World! " + element
                        
# set up pipeline parameters 
parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input',
                      default='gs://dataflow-samples/shakespeare/kinglear.txt')
parser.add_argument('--output', dest='output',
                    default='gs://dsp_model_store/shakespeare/kinglear3.txt')
known_args, pipeline_args = parser.parse_known_args(None)
pipeline_options = PipelineOptions(pipeline_args)

# define the pipeline steps 
p = beam.Pipeline(options=pipeline_options)
lines = p | 'read' >> ReadFromText(known_args.input)
appended = lines | 'append' >> beam.ParDo(AppendDoFn())
appended | 'write' >> WriteToText(known_args.output)

# run the pipeline 
result = p.run()
result.wait_until_finish()

