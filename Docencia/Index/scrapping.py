import urllib, requests
from bs4 import BeautifulSoup
import json

def getMetaDatos(link):
    response = requests.get(link)

    soup =  BeautifulSoup(response.text, "html.parser")

    title = soup.find("meta",  property="og:title")
    url = soup.find("meta",  property="og:url")
    image = soup.find("meta",  property="og:image")
    description = soup.find("meta",  property="og:description")

    jsonfile = {
        "title": "",
        "url": "",
        "image": "",
        "description": ""
    }

    titulo = title["content"] if title else "No meta title given"
    url = url["content"] if url else "No meta url given"

    try:
        image = image["content"] if url else ""
    except TypeError:
        image = ""

    try:
        description = description["content"] if url else ""
    except TypeError:
        description = ""
    
    jsonfile["title"] = titulo
    jsonfile["url"] = url
    jsonfile["image"] = image
    jsonfile["description"] = description
    # jsonfile = json.dumps(jsonfile, ensure_ascii=False)

    return jsonfile
