from Service.utils import function_api_builder, load_schema, refund_user
import boto3
from utils import MediumToMarkdownBuilder, process_event
import requests
import os
import json
import time
import urllib.parse

lambda_ = boto3.client('lambda', region_name='eu-west-1')
s3 = boto3.client('s3', region_name='eu-west-1')
DOCUMENT_STORE_DIST_URL = os.environ["DOCUMENT_STORE_DIST_URL"]
REFUND_LAMBDA = os.environ["REFUND_LAMBDA"]
DOCUMENT_STORE_BUCKET = os.environ["DOCUMENT_STORE_BUCKET"]
print("LAODING")
MediumToMarkdown = MediumToMarkdownBuilder(requests.get)

SERVICE_COST = 1


def handler_builder(s3, bucket_name, lambda_, refund_lambda_name, credits, MediumToMarkdown, process_event, base_location):
    def handler(event, context):
        print(event, context)
        try:
            prev_time = time.time()
            item = process_event(event)
            url = item["url"]
            filename = url[:100]
            print("filename", filename)
            tagging = urllib.parse.urlencode({'Status': 'Temporary'})
            try:
                medium_post = MediumToMarkdown(url)
                print("filename", filename)
                s3_resp = s3.put_object(Body=medium_post, Bucket=bucket_name,
                              Key=f'documents/{item["user"]["id"]}/{filename}', Tagging=tagging)
                print("s3_resp: ", s3_resp)
                time_taken = time.time() - prev_time
                print("time_taken: ", time_taken, url)
            except Exception as err:
                print("FAILED TO GET MEDIUM POST: ", err)
                try:
                    s3.put_object(Body="Failed", Bucket=bucket_name,
                                  Key=f'documents/{item["user"]["id"]}/{filename}', Tagging=tagging)
                    id = item["user"]["id"]
                    refund_user(lambda_, refund_lambda_name)(credits, id=id)
                except Exception as refund_error:
                    print("FAILED TO REFUND USER: ",
                          event, context, refund_error)
        except Exception as err:
            print("FAILED TO PROCESS QUEUE EVENT: ", err)
    return handler


handler = handler_builder(s3, DOCUMENT_STORE_BUCKET, lambda_, REFUND_LAMBDA,
                          SERVICE_COST, MediumToMarkdown, process_event, DOCUMENT_STORE_DIST_URL)
