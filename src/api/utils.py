from urllib import parse
import json 

def ServiceAPIBuilder(sqs_client, sqs_url, check_url, base_location):
  def _func(body):
    url = body["mediumURL"]
    check_url(url)
    user = body["user"]
    response = sqs_client.send_message(QueueUrl=sqs_url, MessageBody=json.dumps({"user": user, "url":url}))
    medium_post_location = f"https://{base_location}/documents/{user['id']}/{url[:100]}"
    return {
      "location": medium_post_location
    }
  return _func

def check_URL(url):
    url_obj = parse.urlsplit(url)
    if not url_obj.netloc.endswith("medium.com"):
        raise Exception('BAD URL')
    return True

