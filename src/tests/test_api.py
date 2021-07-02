import pytest
import json
from ..api.utils import ServiceAPIBuilder, check_URL
import fastjsonschema
import pathlib
BASE = pathlib.Path(__file__).parent.parent
SCHEMA = BASE.joinpath("api/schema")


def load_schema(reference):
    json_data = json.loads(open(SCHEMA.joinpath(
        reference).absolute().as_posix(), 'rb').read().decode('utf-8'))
    return {
        "compiled": fastjsonschema.compile(json_data),
        "raw": json_data
    }


schemas = {
    'input': load_schema('input.json'),
    'output': load_schema('output.json'),
}


class SqsClient:
    def __init__(self):
        return

    def send_message(self, *args, **kwargs):
        return {

        }


sqs_client = SqsClient()
base_location = "document-store.t3chflicks.org"
def check_url(url):
  return True

ServiceApi = ServiceAPIBuilder(sqs_client, "123", check_url, base_location)


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

def test_api():
    resp = ServiceApi({
      "mediumURL": "https://medium.com/@xdamman/my-10-day-meditation-retreat-in-silence-71abda54940e",
      "user": {
        "id": "sk"
      }
    })
    assert resp == {
      "location": "https://document-store.t3chflicks.org/documents/sk/https://medium.com/@xdamman/my-10-day-meditation-retreat-in-silence-71abda54940e"
    }


def test_input_schema_correct():
    input = {"mediumURL": "https://medium.com/@xdamman/my-10-day-meditation-retreat-in-silence-71abda54940e", "key": "123"}
    schemas["input"]["compiled"](input)


@pytest.mark.xfail(raises=Exception)
def test_input_schema_fails():
    input = {"text": "example comment is what up bro"}
    schemas["input"]["compiled"](input)


def test_output_schema_correct():
    output = {"location": 'https://document-store.t3chflicks.org/medium-to-markdown/https://medium.com/@xdamman/my-10-day-meditation-retreat-in-silence-71abda54940e'}
    schemas["output"]["compiled"](output)


@pytest.mark.xfail(raises=Exception)
def test_output_schema_fails():
    output = {"keywords": [{"word": "t3chflicks", "score": 0.7}]}
    schemas["output"]["compiled"](output)

def test_url_checker():
    title= "medium url checker checks medium urls"
    good_URL = "https://t3chflicks.medium.com/aws-solutions-architect-quiz-6-iam-5d34116f3c73"
    result = check_URL(good_URL)
    assert result == True

@pytest.mark.xfail(raises=Exception)
def test_url_checker_fail():
    title= "medium url checker checks bad urls"
    good_URL = "https://mysite.com/aws-solutions-architect-quiz-6-iam-5d34116f3c73"
    result = check_URL(good_URL)
    assert result == True