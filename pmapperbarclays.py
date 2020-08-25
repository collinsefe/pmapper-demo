import argparse
from principalmapper.analysis import find_risks
from principalmapper.graphing import graph_actions
from principalmapper.graphing.edge_identification import checker_map
from principalmapper.util import botocore_tools
from principalmapper.visualizing import graph_writer
import s3util
from datetime import datetime

# Added by Collins
BUCKET_NAME = "corighose-pmapper"
BUCKET_REGION = "us-east-1"
LOCAL_STORAGE_PATH = "/tmp/"

def lambda_handler(event, context):
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', default='default')
    parser.add_argument('--format', default='text', choices=['text', 'json'])
    
    #parsed_args = parser.parse_args(["None"])
    parsed_args = parser.parse_args()
    session = botocore_tools.get_session(parsed_args.profile)
    graph_obj = graph_actions.create_new_graph(session, checker_map.keys())
    
    dateNow = datetime.now()
    unique_outputFile = "output_" + dateNow.strftime("%H-%M-%S-%f")
    s3ObjectName = unique_outputFile + ".png"

    create_signed_URL(s3ObjectName)

    filePath = LOCAL_STORAGE_PATH + s3ObjectName
    graph_writer.handle_request(graph_obj,filePath,"png")
    uploaded = s3util.upload_to_s3(filePath,BUCKET_NAME,s3ObjectName)
    return uploaded
    



def create_signed_URL(outputObjectName):
    
    response = s3util.create_presigned_url(BUCKET_NAME, outputObjectName, BUCKET_REGION)
    return print(response)

if __name__ == '__main__':
    lambda_handler(None, None)


