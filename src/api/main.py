from Service.utils import function_api_builder, load_schema
import boto3
from utils import ServiceAPIBuilder, check_URL
import os

DOCUMENT_STORE_DIST_URL = os.environ["DOCUMENT_STORE_DIST_URL"]
SQS_URL = os.environ["SQS_URL"]
client = boto3.client('sqs', region_name='eu-west-1')
print("LOADING")
ServiceAPI = ServiceAPIBuilder(client, SQS_URL, check_URL, DOCUMENT_STORE_DIST_URL)
print("create funcs")

schema_path = "schema/"
input_schema = load_schema(f'{schema_path}input.json')
output_schema = load_schema(f'{schema_path}output.json')
lambda_ = boto3.client('lambda', region_name='eu-west-1')
credits = 1
charge_lambda_name = os.environ['CHARGE_LAMBDA']
refund_lambda_name = os.environ['REFUND_LAMBDA']
handler = function_api_builder(input_schema, output_schema, lambda_, charge_lambda_name, refund_lambda_name, credits, ServiceAPI)

