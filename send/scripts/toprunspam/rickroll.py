import asyncio
import random
import re
import sys

import httpx
from generator import *

from player_pb2 import PlayerResponse, UpdatePlayerRequest

api_url = "https://subwaycity.prod.sybo.net"
user_agent = "grpc-dotnet/2.63.0 (Mono Unity; CLR 4.0.30319.17020; netstandard2.0; arm64) com.kiloo.subwaysurf/3.46.9"

RICKROLL_NAMES = [
    "Never",
    "gonna",
    "give",
    "you",
    "up",
    "Never",
    "gonna",
    "let",
    "you",
    "down",
    "Never",
    "gonna",
    "run",
    "around",
    "And",
    "desert",
    "you",
    "Never",
    "gonna",
    "make",
    "you",
    "cry",
    "Never",
    "gonna",
    "say",
    "goodbye",
    "Never",
    "gonna",
    "tell",
    "a",
    "lie",
    "And",
    "hurt",
    "you",
]


def framing(msg):
    payload = msg.SerializeToString()
    return b"\x00" + len(payload).to_bytes(4, "big") + payload


async def auth_register(client):
    url = api_url + "/v2.0/auth/register"
    r = await client.post(url, headers={"Content-Type": "application/json"})
    r.raise_for_status()
    return r.json()


async def create_player(client, authtoken, name):
    AvatarKey = f"Avatar{random.randint(1,14)}"
    surfer = choose_surfer()

    msg = UpdatePlayerRequest(
        name=name,
        level=random.randint(1, 50),
        highscore=random.randint(1, 50000),
        metadata={
            "HighScoreCharacterKey": f"DataTag({str(surfer)})",
            "AvatarKey": AvatarKey,
        },
    )

    body = framing(msg)

    headers = {
        "User-Agent": user_agent,
        "grpc-accept-encoding": "identity,gzip",
        "Authorization": f"Bearer {authtoken}",
        "Content-Type": "application/grpc-web",
    }

    url = api_url + "/rpc/player.ext.v1.PrivateService/CreatePlayer"

    r = await client.post(url, headers=headers, content=body)

    raw = r.content
    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    resp = PlayerResponse()
    resp.ParseFromString(grpc_payload)

    return resp


async def send_scores(
    client, authtoken, playername: str, score: int, character: int, country: str
):
    url = api_url + "/rpc/leaderboard.ext.v1.PrivateService/SubmitScore"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {authtoken}",
    }

    body = {
        "leaderboard": {
            "id": "top_run_weekly_v2",
            "partitions": {
                "partitionStrings": [{"key": "cc", "value": country.lower()}],
                "partitionIntegers": [{"key": "lvl", "value": 50}],
            },
        },
        "score": {
            "value": str(score),
            "metadata": [
                {"key": "playerName", "value": playername},
                {"key": "characterName", "value": str(character)},
            ],
        },
    }

    await client.post(url, headers=headers, json=body)


async def worker(
    client,
    name: str,
    counter: int,
    country: str = "us",
    score: str = "2147483647",
    character: int = "-1534276928",
    avatar: int = None,
):
    try:
        print(name)
        """
        auth = await auth_register(client)
        authtoken = auth["idToken"]

        await create_player(client, authtoken, name)
        await send_scores(client, authtoken, name, score, character, country)
        """

        counter["remaining"] -= 1
        print("Remaining:", counter["remaining"])

    except Exception as e:
        print("Error:", e)


async def main(amount, country):
    counter = {"remaining": amount}
    countries = get_countrys()
    if country not in [c["code"].lower() for c in countries]:
        print("Invalid country code")
        return

    limits = httpx.Limits(max_connections=100, max_keepalive_connections=50)

    async with httpx.AsyncClient(http2=True, limits=limits, timeout=20) as client:
        ordered_names = [RICKROLL_NAMES[i % len(RICKROLL_NAMES)] for i in range(amount)]
        tasks = [worker(client, n, counter, country) for n in ordered_names]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <amount> <country>")
        sys.exit(1)

    amount = int(sys.argv[1])
    country = sys.argv[2].lower()

    try:
        asyncio.run(main(amount, country))
    except KeyboardInterrupt:
        print("\nExiting.")
