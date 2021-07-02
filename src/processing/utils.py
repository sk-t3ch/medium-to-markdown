
import re
from datetime import datetime
import json
from io import BytesIO
MEDIUM_IMG_CDN = "https://cdn-images-1.medium.com/max/"


def MediumToMarkdownBuilder(request_get):
    def _func(url):
        print("URL: ", url)
        medium_post = load_medium_json(request_get)(url)
        print("MEDIUM POST: ", medium_post["type"])
        if (medium_post["type"] != "Post"):
            raise Exception('Not a Medium Article')

        story = {}
        story["title"] = medium_post["title"]
        story["date"] = datetime.fromtimestamp(
            medium_post["createdAt"]/1000).timestamp()

        story["sections"] = medium_post["content"]["bodyModel"]["sections"]
        story["paragraphs"] = medium_post["content"]["bodyModel"]["paragraphs"]
        print("SECTIONS: ", story["sections"])
        sections = [process_section(s) for s in story["sections"]]
        if (len(story["paragraphs"]) > 1):
            story["subtitle"] = story["paragraphs"][1]["text"]

        story["markdown"] = []
        story["markdown"].append(
            "# " + story["title"].replace(r'/\n/g', '\n# '))
        subtitle = story.get("subtitle", False)
        if subtitle and subtitle != "":
            story["markdown"].append(
                "\n" + story["subtitle"].replace(r'/#+/', ''))
        print("SECTIONS:L ", sections)
        sections_len = len(sections)
        for para_idx, paragraph in enumerate(story["paragraphs"]):
            if para_idx < 2:
                continue
            if (para_idx < sections_len):
                story["markdown"].append(sections[para_idx])
            p = story["paragraphs"][para_idx]
            processed_paragraph = process_paragraph(request_get)(p)
            print(f"{para_idx}#####: " + processed_paragraph)
            story["markdown"].append(processed_paragraph)
        markdown = '\n'.join(story["markdown"])
        return markdown
        # return {
        #     "markdown": markdown,
        #     "size": len(markdown.encode('utf-8')),
        #     "title": story["title"],
        #     "date": story["date"]
        # }
    return _func


def load_medium_json(fetch):
    def _func(url):
        headers = {"cookie": "uid=c6b26bf1493d; sid=1:Cpecb3c0Gw3/muTeOivJg4LclDQILLd4jxeO2T5s71a3uolNKV4OrMjWW7LAraLC; xsrf=d7f515c978f3;"}
        payload = {'format': 'json'}
        response = fetch(url, params=payload, headers=headers)
        print("RESPONSE: ", response)
        text = response.text
        print("text: ", text)
        result = json.loads(text[text.index('{'):])["payload"]["value"]
        print("result: ", result)
        return result
    return _func


def process_section(s):
    section = ""
    background_image = s.get("backgroundImage", False)
    if (background_image):
        img_width = int(background_image["originalWidth"])
        img_src = f"{MEDIUM_IMG_CDN}{max(img_width * 2, 2000)}/{background_image['id']}"
        section = "\n![](" + img_src + ")"
    return section


def get_embed(fetch):
    def _func(url):
        # determine if youtube url or github
        embed = ""
        embed_json = load_medium_json(fetch)(url)
        # print(embed_json.keys())
        if (embed_json["domain"] in ["www.github.com", "gist.github.com"]):
            embed = get_GitHub_embed(fetch)(embed_json)
            # print("### summin", embed)

        elif (embed_json["domain"] == "www.youtube.com"):
            embed = get_YouTube_embed(embed_json)
        else:
            print("WTF")
        return embed
    return _func


def get_GitHub_embed(fetch):
    def _func(embed_json):
        try:
            md_soure_code = ''
            # print("TRYING")
            if (embed_json["gist"]):
                gist = embed_json["gist"]
                # print("GIST: ", gist)

                script_src = f"https://api.github.com/gists/{gist['gistId']}"
                gist_json_resp = fetch(script_src)
                # print(gist['gistId'])
                # print(gist_json_resp)
                gist_json = gist_json_resp.json()

                for file in gist_json["files"].values():
                    language = file["language"]
                    language = language.lower() if language is not None else ""
                    gist_code_resp = fetch(file["raw_url"])
                    gist_code = gist_code_resp.text
                    md_soure_code += ('\n```' + language + '\n')
                    md_soure_code += gist_code.replace(r'/\t/g', '  ')
                    md_soure_code += '\n```\n'

                if (len(md_soure_code) > 0):
                    # TOODO find subvstring method
                    # print("d", len(md_soure_code) - 1)
                    md_soure_code = md_soure_code[:len(md_soure_code) - 1]

                # with open(f"md_source_code_{gist['gistId']}.json", "w+") as f:
                #     f.write(md_soure_code)

            return md_soure_code
        except Exception as err:
            print("ERR: ", err)
            return ""
    return _func


def get_YouTube_embed(embed_json):
    body = embed_json["iframeSrc"]
    regex = r"youtube.com%2Fembed%2F([^%]+)%3F"
    matches = re.search(regex, body)
    if (matches and len(matches.groups()) >= 1):
        video_id = matches.groups(1)[0]
        return f"<center><iframe width='560' height='315' src ='https://www.youtube.com/embed/${video_id}' frameborder='0' allowfullscreen></iframe></center>"
    return f"<iframe src='{body}' frameborder=0></iframe>"


def process_paragraph(fetch):
    def _func(p):
        markups_array = create_markups_array(p["markups"])

        if (len(markups_array)):
            previous_index = 0
            text = p["text"]
            tokens = []
            for j_index, markup in enumerate(markups_array):
                if (markup is not None):
                    token = text[previous_index: j_index]
                    previous_index = j_index
                    tokens.append(token)
                    tokens.append(markup)
            tokens.append(text[j_index:])
            p["text"] = ''.join(tokens)
        markup = ""
        if p["type"] == 1:
            markup = "\n"
        elif p["type"] == 2:
            p["text"] = "\n# " + p["text"].replace(r'/\n/g', '\n# ')
        elif p["type"] == 3:
            p["text"] = "\n## " + p["text"].replace(r'/\n/g', '\n## ')
        elif p["type"] == 4:
            # image & caption
            img_width = int(p["metadata"]["originalWidth"])
            img_src = f"{MEDIUM_IMG_CDN}{max(img_width * 2, 2000)}/{p['metadata']['id']}"
            text = "\n![" + p["text"] + "](" + img_src + ")"
            if (p["text"]):
                text += "*\n\n" + p["text"] + "*"
            p["text"] = text
        elif p["type"] == 6:
            markup = "> "
        elif p["type"] == 7:
            # quote
            p["text"] = "> # " + p["text"].replace('\n', '\n> # ')
        elif p["type"] == 8:
            p["text"] = "\n    " + p["text"].replace('\n', '\n    ')
        elif p["type"] == 9:
            markup = "\n* "
        elif p["type"] == 10:
            markup = "\n1. "
        elif p["type"] == 11:
            mediaURL = f"https://medium.com/media/{p['iframe']['mediaResourceId']}"
            embed = get_embed(fetch)(mediaURL)
            # print("EMBED: ", embed)
            return f"\n{ embed }"
        elif p["type"] == 13:
            markup = "\n### "
        elif p["type"] == 15:
            # // caption for section image
            p["text"] = "*" + p["text"] + "*"

        p["text"] = markup + p["text"]

        if (p.get("alignment", False) == 2 and p["type"] != 6 and p["type"] != 7):
            p["text"] = "<center>" + p["text"] + "</center>"

        return p["text"]
    return _func


def add_markup(markups_array, open, close, start, end):
    if markups_array[start]:
        markups_array[start] += open
    else:
        markups_array[start] = open

    if markups_array[end]:
        markups_array[end] += close
    else:
        markups_array[end] = close
    return markups_array


def create_markups_array(markups):
    if (not markups or len(markups) == 0):
        return []
    markups_array = [None] * (max(map(lambda x: x["end"], markups))+1)
    for m in markups:
        if m["type"] == 1:
            # // bold
            add_markup(markups_array, "**", "**", m["start"], m["end"])
        elif m["type"] == 2:
            # // italic
            add_markup(markups_array, "*", "*", m["start"], m["end"])
        elif m["type"] == 3:
            # // anchor tag
            add_markup(markups_array, "[", "](" +
                       m["href"] + ")", m["start"], m["end"])
        elif m["type"] == 8:
            # // code tag
            add_markup(markups_array, "```", "```", m["start"], m["end"])
        elif m["type"] == 10:
            # // code tag
            add_markup(markups_array, "`", "`", m["start"], m["end"])
        else:
            print("Unknown markup type " + m["type"], m)
    return markups_array

def process_event(event):
    record = event['Records'][0]
    result = json.loads(record['body'])
    return result