"""
This script should test 3rd party APIs to see if their response is as we expect
"""
import pytest
import json
from ..processing.utils import MediumToMarkdownBuilder, \
    load_medium_json, get_GitHub_embed, \
    get_YouTube_embed 
import os

import requests

base_location = "https://document-store.t3chflicks.org/medium-to-markdown/"


with open('fixtures/article_json/youtube-embed.json') as f:
    youtube_embed_json = json.loads(f.read())

with open('fixtures/article_markdown/gist.md') as f:
    github_markdown = f.read()

with open('fixtures/other/gist.txt') as f:
    github_test = f.read()

with open('fixtures/other/medium-queue-event.json') as f:
    example_event = json.loads(f.read())

with open('fixtures/article_json/github-embed.json') as f:
    medium_github_json = json.loads(f.read())

# def test_get_GitHub_embed():
#     func = get_GitHub_embed(requests.get)
#     resp = func(medium_github_json)
#     assert resp == github_markdown


def test_get_YouTube_embed():
    resp = get_YouTube_embed(youtube_embed_json)
    # print("RESP: ", resp)
    assert resp == "<center><iframe width='560' height='315' src ='https://www.youtube.com/embed/$rkmM_F-sD38' frameborder='0' allowfullscreen></iframe></center>"
