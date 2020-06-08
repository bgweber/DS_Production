import apache_beam as beam
import argparse
from apache_beam.options.pipeline_options import PipelineOptions

# define a function for transforming the data 
class AppendDoFn(beam.DoFn):
    def process(self, element):
        print("Hellow World! - " + element)
        
# set up pipeline parameters 
parser = argparse.ArgumentParser()
known_args, pipeline_args = parser.parse_known_args(None)
pipeline_options = PipelineOptions(pipeline_args)

# define the topics 
topic = "projects/{project}/topics/{topic}"
topic = topic.format(project = "gameanalytics-199018", topic = "natality")


# define the pipeline steps 
p = beam.Pipeline(options=pipeline_options)
lines = p | 'Read PubSub' >> beam.io.ReadFromPubSub(topic=topic)
appended = lines | 'append' >> beam.ParDo(AppendDoFn())

# run the pipeline 
result = p.run()
result.wait_until_finish()
