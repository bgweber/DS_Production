
import argparse
import apache_beam as beam

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions

# define a function for transforming the data 
class AppendDoFn(beam.DoFn):
    def process(self, element):
        print("Hello World! - " + element.decode('utf-8'))
        
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
 | 'Append' >> beam.ParDo(AppendDoFn()))

# run the pipeline 
result = p.run()
result.wait_until_finish()
