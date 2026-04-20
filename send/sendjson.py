import base64
import json
import os
import re
import urllib.parse
from typing import Optional, Tuple, Union

import httpx
from dotenv import load_dotenv

api_url = "https://subwaycity.prod.sybo.net"
manifest_api_url = "https://manifest.tower.sybo.net"
gamedata_api_url = "https://gamedata.tower.sybo.net"


load_dotenv()
identityToken = os.getenv("IDENTITYTOKEN", "")

headers = {
    "User-Agent": "Subway Surf/3.47.0 (Android OS 13 / API-33 (TKQ1.230127.002/TP2R)) Android)",
    "TE": "trailers",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip",
}


def auth_register():
    url = api_url + "/v2.0/auth/register"

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={"Content-Type": "application/json"},
        )

        response_json = r.json()

        print(response_json)


# Needs Authtoken
def auth_refresh(refreshToken: str):
    url = api_url + "/v2.0/auth/refresh"

    data = {"refreshToken": refreshToken, "fbAccessToken": None}

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
            json=data,
        )

        response_json = r.json()
        idToken = response_json.get("idToken", "idToken not found")
        idTokenTtl = response_json.get("idTokenTtl", "idToken not found")
        refreshToken = response_json.get("refreshToken", "idToken not found")
        user = response_json.get("user", "user not found")
        user_id = user.get("id", "id not found")
        links = user.get("links", "links not found")

        print(response_json)


# Needs Authtoken
def get_mail(
    payer: bool = False,
    level: int = 0,
    age: int = 65,
    language: str = "en",
    platform: str = "android",
    coppa: bool = True,
    version: str = "3.47.0",
):
    url = api_url + "/v2.0/mail"

    data = {
        "language": language,
        "metrics": {
            "payer": str(payer),
            "level": str(level),
            "language": language,
            "age": str(age),
            "platform": platform,
            "coppa": str(coppa),
            "gameVersion": version,
        },
    }
    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
            json=data,
        )

        print(r.json())


def get_manifest(
    manifestSecret: str,
    version: str,
    game: str = "subwaycity",
    type: str = "android",
    experiment: Optional[str] = None,
):
    if type not in ["android", "ios"]:
        raise ValueError("Invalid type. Must be 'android' or 'ios'.")
    if not manifestSecret:
        raise ValueError("manifestSecret is required.")
    if not version:
        raise ValueError("version is required.")

    experiment_path = f"/{experiment}" if experiment else ""
    url = f"{manifest_api_url}/v1.0/{game}/{version}/{type}/{manifestSecret}{experiment_path}/manifest.json"

    with httpx.Client(http2=True) as client:
        r = client.get(url, headers=headers)
        r.raise_for_status()
        print(r.json())


def get_gamedata(
    game: str = "subwaycity",
    gamedataSecret: Optional[str] = None,
    file: Optional[str] = None,
):
    if not game:
        raise ValueError("game is required.")
    if not gamedataSecret:
        raise ValueError("manifestSecret is required.")
    if not file:
        raise ValueError("file is required.")

    filename = file.replace(".json", "")
    url = gamedata_api_url + f"/v1.0/{game}/{gamedataSecret}/{filename}.json"

    with httpx.Client(http2=True) as client:
        r = client.get(
            url,
            headers=headers,
        )

        r.raise_for_status()

        print(r.json())


# Needs Authtoken
def gdpr_delete(gaid: str):
    url = api_url + "/v1.0/gdpr/delete"

    data = {"idfa": None, "gaid": gaid}

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
            json=data,
        )

        print(r.json())


# Needs Authtoken
def gdpr_status():
    url = api_url + "/v1.0/gdpr/status"

    with httpx.Client(http2=True) as client:
        r = client.get(
            url,
            headers={
                **headers,
                "Authorization": f"Bearer {identityToken}",
            },
        )

        print(r.json())


def get_when():
    url = "https://when.sybo.net"

    with httpx.Client(http2=True) as client:
        r = client.get(
            url,
            headers=headers,
        )
        r.raise_for_status()

        print(r.json())


def get_where():
    url = "https://where.sybo.net"

    with httpx.Client(http2=True) as client:
        r = client.get(
            url,
            headers=headers,
        )
        r.raise_for_status()

        print(r.json())


# auth_register()
# get_mail()
# auth_refresh("")
# get_manifest(manifestSecret="s8B88pVbhzpKmvX6BV0u", game="subway",type="android",experiment="ab_google_play",version="3.44.2")
# get_gamedata("657db86da87f6e2625b1de17aaa7017975ff032f", "manifest")
# gdpr_delete()
# gdpr_status()
# get_when()
# get_where()
