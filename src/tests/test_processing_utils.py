import pytest
import json
from ..processing.utils import MediumToMarkdownBuilder, \
    load_medium_json, process_section, get_GitHub_embed, \
    get_YouTube_embed, process_paragraph, \
    create_markups_array, process_event
import os
# import fastjsonschema
# import pathlib
# BASE = pathlib.Path(__file__).parent.parent
# SCHEMA = BASE.joinpath("api/schema")


# def load_schema(reference):
#     json_data = json.loads(open(SCHEMA.joinpath(
#         reference).absolute().as_posix(), 'rb').read().decode('utf-8'))
#     return {
#         "compiled": fastjsonschema.compile(json_data),
#         "raw": json_data
#     }


# schemas = {
#     'input': load_schema('input.json'),
#     'output': load_schema('output.json'),
# }


# class SqsClient:
#     def __init__(self):
#         return

#     def put(self, item):
#         print(item)
#         return {

#         }


# sqs_client = SqsClient()
base_location = "https://document-store.t3chflicks.org/medium-to-markdown/"
with open('fixtures/article_json/how-to-use-amplify-auth-in-nuxt.txt') as f:
    medium_text_response = f.read()

with open('fixtures/article_json/how-to-use-amplify-auth-in-nuxt-text.json') as f:
    medium_json_response = json.loads(f.read())

with open('fixtures/article_markdown/how-to-use-amplify-auth-in-nuxt.md') as f:
    medium_markdown = f.read()

with open('fixtures/article_json/github-embed.json') as f:
    medium_github_json = json.loads(f.read())

with open('fixtures/article_json/gist-github-response.json') as f:
    github_json = json.loads(f.read())

with open('fixtures/article_json/youtube-embed.json') as f:
    youtube_embed_json = json.loads(f.read())

with open('fixtures/article_markdown/gist.md') as f:
    github_markdown = f.read()

with open('fixtures/other/gist.txt') as f:
    github_test = f.read()

with open('fixtures/other/medium-queue-event.json') as f:
    example_event = json.loads(f.read())


class RequestGetResponse:
    def __init__(self):
        self.text = medium_text_response

def request_get(url, *args, **kwargs):
    return RequestGetResponse()


class FetchGithubResponse:
    def __init__(self):
        self.text = github_test

    def json(self):
        return github_json

def fetch_github(url):
    return FetchGithubResponse()


MediumToMarkdown = MediumToMarkdownBuilder(request_get)


class test_lambda_success:
    def __init__(self):
        pass

    def invoke(self, params):
        return {"StatusCode": "200", "Payload": json.dumps({})}


class test_lambda_failure:
    def __init__(self):
        pass

    def invoke(self, params):
        raise Exception('ha')


class test_lambda_failure_toggle:
    def __init__(self):
        self.x = False

    def invoke(self, params):
        if(self.x == True):
            raise Exception('ha')
        else:
            self.x = True
            return {"Payload": "1", "StatusCode": "200"}


lambda_success = test_lambda_success()
lambda_failure = test_lambda_failure()



def test_load_medium_json():
    medium_json = load_medium_json(request_get)(
        "https://medium.com/@xdamman/my-10-day-meditation-retreat-in-silence-71abda54940e")
    assert medium_json == medium_json_response


def test_process_section():
    resp = process_section({
        "backgroundImage": {
            "originalWidth": 10,
            "id": "sauce"
        }
    })
    assert resp == '\n![](https://cdn-images-1.medium.com/max/2000/sauce)'


def test_get_GitHub_embed():
    func = get_GitHub_embed(fetch_github)
    resp = func(medium_github_json)
    assert resp == github_markdown


def test_get_YouTube_embed():
    resp = get_YouTube_embed(youtube_embed_json)
    # print("RESP: ", resp)
    assert resp == "<center><iframe width='560' height='315' src ='https://www.youtube.com/embed/$rkmM_F-sD38' frameborder='0' allowfullscreen></iframe></center>"


def test_process_paragraph():
    title = "converts a paragraph with an anchor tag to markdown"
    p = {
        "name": "e93e",
        "type": 1,
        "text": "The next step for you reader is to install an ad blocker for your browser. I recommend uBlock. Also Pocket or Instapaper are great apps to read content from publishers without having to load their website again and again.",
        "markups": [
            {
                "type": 3,
                "start": 87,
                "end": 93,
                "href": "http://ublock.org",
                "title": "",
                "rel": "",
                "anchorType": 0
            },
            {
                "type": 3,
                "start": 100,
                "end": 106,
                "href": "http://getpocket.com",
                "title": "",
                "rel": "",
                "anchorType": 0
            },
            {
                "type": 3,
                "start": 110,
                "end": 120,
                "href": "http://instapaper.com",
                "title": "",
                "rel": "",
                "anchorType": 0
            }
        ]
    }
    result = process_paragraph(None)(p)
    assert result == "\nThe next step for you reader is to install an ad blocker for your browser. I recommend [uBlock](http://ublock.org). Also [Pocket](http://getpocket.com) or [Instapaper](http://instapaper.com) are great apps to read content from publishers without having to load their website again and again."


def test_process_paragraph_anchor():
    title = "converts a paragraph with an anchor tag to markdown"
    p = {
        "name": "e93e",
        "type": 1,
        "text": "The next step for you reader is to install an ad blocker for your browser. I recommend uBlock. Also Pocket or Instapaper are great apps to read content from publishers without having to load their website again and again.",
        "markups": [
            {
                "type": 3,
                "start": 87,
                "end": 93,
                "href": "http://ublock.org",
                "title": "",
                "rel": "",
                "anchorType": 0
            },
            {
                "type": 3,
                "start": 100,
                "end": 106,
                "href": "http://getpocket.com",
                "title": "",
                "rel": "",
                "anchorType": 0
            },
            {
                "type": 3,
                "start": 110,
                "end": 120,
                "href": "http://instapaper.com",
                "title": "",
                "rel": "",
                "anchorType": 0
            }
        ]
    }
    result = process_paragraph(None)(p)
    assert result == "\nThe next step for you reader is to install an ad blocker for your browser. I recommend [uBlock](http://ublock.org). Also [Pocket](http://getpocket.com) or [Instapaper](http://instapaper.com) are great apps to read content from publishers without having to load their website again and again."


def test_process_paragraph_multiple():
    title = "converts a paragraph with multiple markups to markdown"
    p = {
        "name": "d827",
        "type": 1,
        "text": "I’ve always been interested in meditation but I’ve never practiced it. I’m just too lazy. I bought the book “Search Inside Yourself” (by Chade-Meng Tan, a Google engineer), read the first chapter and stopped (like I do with most books). I knew that if I wanted to be serious about this I should put myself in a situation where I wouldn’t have any other alternative than to just do it. That’s how I work. So I signed up for 10-day Vipassana Meditation Retreat in Dhamma Manda, 3 hours north of San Francisco, April 15th 2015.",
        "markups": [
            {
                "type": 3,
                "start": 109,
                "end": 131,
                "href": "http://www.amazon.com/Search-Inside-Yourself-Unexpected-Achieving/dp/0062116932",
                "title": "",
                "rel": "",
                "anchorType": 0
            },
            {
                "type": 3,
                "start": 462,
                "end": 474,
                "href": "http://www.manda.dhamma.org/",
                "title": "",
                "rel": "",
                "anchorType": 0
            }
        ]
    }
    result = process_paragraph(None)(p)
    assert result == "\nI’ve always been interested in meditation but I’ve never practiced it. I’m just too lazy. I bought the book “[Search Inside Yourself](http://www.amazon.com/Search-Inside-Yourself-Unexpected-Achieving/dp/0062116932)” (by Chade-Meng Tan, a Google engineer), read the first chapter and stopped (like I do with most books). I knew that if I wanted to be serious about this I should put myself in a situation where I wouldn’t have any other alternative than to just do it. That’s how I work. So I signed up for 10-day Vipassana Meditation Retreat in [Dhamma Manda](http://www.manda.dhamma.org/), 3 hours north of San Francisco, April 15th 2015."


def test_process_paragraph_image():
    title = "converts a paragraph with an image"
    p = {
        "name": "b25e",
        "type": 4,
        "text": "The Dhamma Manda Vipassana Meditation Center in North California (near Kelseyville) (Photo Dhamma Manda on Facebook)",
        "markups": [
            {
                "type": 3,
                "start": 91,
                "end": 115,
                "href": "http://facebook.com/DhammaManda",
                "title": "",
                "rel": "",
                "anchorType": 0
            }
        ],
        "layout": 1,
        "metadata": {
            "id": "1*peNGm67ELigNQtSx4WUoaQ.jpeg",
            "originalWidth": 843,
            "originalHeight": 564
        }
    }
    result = process_paragraph(None)(p)
    assert result == "\n![The Dhamma Manda Vipassana Meditation Center in North California (near Kelseyville) (Photo [Dhamma Manda on Facebook](http://facebook.com/DhammaManda))](https://cdn-images-1.medium.com/max/2000/1*peNGm67ELigNQtSx4WUoaQ.jpeg)*\n\nThe Dhamma Manda Vipassana Meditation Center in North California (near Kelseyville) (Photo [Dhamma Manda on Facebook](http://facebook.com/DhammaManda))*"


def test_process_paragraph_important_quote():
    title = "converts a paragraph with an important quote that includes an anchor tag to markdown"
    p = {
        "name": "6235",
        "type": 7,
        "text": "Test assertions should be dead simple,\n& completely free of magic.",
        "markups": [
            {
                "type": 3,
                "start": 41,
                "end": 65,
                "href": "https://en.wikipedia.org/wiki/Magic_(programming)",
                "title": "",
                "rel": "",
                "anchorType": 0
            }
        ]
    }
    result = process_paragraph(None)(p)
    # print("RESULT: ###", result)
    assert result == "> # Test assertions should be dead simple,\n> # & [completely free of magic](https://en.wikipedia.org/wiki/Magic_(programming))."


def test_process_paragraph():
    title = "converts a paragraph with code highlighted segment"
    p = {
        "name": "86b6",
        "type": 1,
        "text": "/generate-key — this regenerates the User’s API key",
        "markups": [
            {
                "type": 10,
                "start": 0,
                "end": 13
            }
        ]
    }
    result = process_paragraph(None)(p)
    assert result == "\n`/generate-key` — this regenerates the User’s API key"


def test_process_paragraph():
    title = "converts a paragraph with code excerpt to markdown"
    p = {
        "name": "6750",
        "type": 8,
        "text": "TAP version 13\n# A passing test\nok 1 This test will pass.\n# Assertions with tape.\nnot ok 2 Given two mismatched values, .equal() should produce a nice bug report\n  ---\n    operator: equal\n    expected: 'something to test'\n    actual:   'sonething to test'\n  ...",
        "markups": []
    }
    result = process_paragraph(None)(p)
    assert result == '\n    TAP version 13\n    # A passing test\n    ok 1 This test will pass.\n    # Assertions with tape.\n    not ok 2 Given two mismatched values, .equal() should produce a nice bug report\n      ---\n        operator: equal\n        expected: \'something to test\'\n        actual:   \'sonething to test\'\n      ...'


def test_process_paragraph():
    title = "creates the markups array"
    p = {
        "name": "6235",
        "type": 7,
        "text": "Test assertions should be dead simple,\n& completely free of magic.",
        "markups": [
            {
                "type": 3,
                "start": 41,
                "end": 65,
                "href": "https://en.wikipedia.org/wiki/Magic_(programming)",
                "title": "",
                "rel": "",
                "anchorType": 0
            }
        ]
    }
    markups_array = create_markups_array(p["markups"])
    assert len(markups_array) > 0


def test_process_event():
    result = process_event(example_event)
    expected = {
        "url": "https://t3chflicks.medium.com/home-devops-pipeline-a-junior-engineers-tale-2-4-7be3e3c292c",
        "user": {
            "id":  "Google_115762588010536765520"
        }
    }
    assert result == expected
