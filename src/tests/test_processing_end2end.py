"""
This script should test that the processing works end to end - from the sqs event to 
the response being available.
"""
import pytest
import json
from ..processing.utils import MediumToMarkdownBuilder
import os
import requests
with open('./fixtures/article_json/pay-me-quickstart-for-creating-a-saas-pt-2-stripe-payments.txt') as f:
    medium_text_response = f.read()
with open('./fixtures/article_markdown/pay-me-quickstart-for-creating-a-saas-pt-2-stripe-payments.md') as f:
    medium_markdown = f.read()

class RequestGetResponse:
    def __init__(self):
        self.text = medium_text_response

def request_get(url):
    return RequestGetResponse()

MediumToMarkdown = MediumToMarkdownBuilder(request_get)

# def test_processing():
#     name = 'pay-me-quickstart-for-creating-a-saas-pt-2-stripe-payments'
#     # with open(f'./fixtures/article_json/{name}.json') as f:
#     #     article_json = json.loads(f.read())
   
#     # with open(f'./fixtures/article_markdown/{name}.md') as f:
#     #     article_md = f.read()
#     url = 'https://t3chflicks.medium.com/pay-me-quickstart-for-creating-a-saas-pt-2-stripe-payments-44bc4bb8388e'
#     # resp = MediumToMarkdownBuilder(requests.get)(url)
#     # with open(f'./fixtures/article_markdown/test/{name}.md', 'w+') as f:
#     #     f.write(resp)
#     # assert resp == medium_markdown
#     # assert resp == 0

# def test_processing():
#     name = 'catboost-quickstart-ml-classification'
#     with open('./fixtures/article_markdown/catboost-quickstart-ml-classification.md') as f:
#         medium_markdown = f.read()
   
#     # with open(f'./fixtures/article_markdown/{name}.md') as f:
#     #     article_md = f.read()
#     url = 'https://t3chflicks.medium.com/catboost-quickstart-ml-classification-f1d7fb70fea8'
#     resp = MediumToMarkdownBuilder(requests.get)(url)
#     with open(f'./fixtures/article_markdown/test/{name}.md', 'w+') as f:
#         f.write(resp)
#     assert resp == medium_markdown


# TODO: fix links to other articles
# TODO: fix bold and italic together in wrong pos

# def test_processing():
#     with open('./fixtures/article_markdown/solution_architect_6.md') as f:
#         medium_markdown = f.read()
   
#     # with open(f'./fixtures/article_markdown/{name}.md') as f:
#     #     article_md = f.read()
#     url = 'https://t3chflicks.medium.com/aws-solutions-architect-quiz-6-iam-5d34116f3c73'
#     resp = MediumToMarkdownBuilder(requests.get)(url)
#     with open(f'./fixtures/article_markdown/test/solution_architect_6.md', 'w+') as f:
#         f.write(resp)
#     assert resp == medium_markdown