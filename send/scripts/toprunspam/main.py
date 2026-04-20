import argparse
import asyncio
import random
import re
import sys

import httpx

from generator import *
from player_pb2 import PlayerResponse, UpdatePlayerRequest

api_url = "https://subwaycity.prod.sybo.net"
user_agent = "grpc-dotnet/2.63.0 (Mono Unity; CLR 4.0.30319.17020; netstandard2.0; arm64) com.kiloo.subwaysurf/3.46.9"
LEVELS = [20, 30, 40, 50]


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


async def create_player(client, authtoken, name, surfer, avatar, score, level):
    if avatar:
        AvatarKey = f"Avatar{avatar}"
    else:
        AvatarKey = f"Avatar{random.choice([random.randint(1, 14), ''])}"
    AvatarKey = f"Avatar"

    # surfer = choose_surfer() if not surfer else surfer
    surfer = "-1534276928"

    level = random.randint(0, 50) if not level else level
    highscore = random.randint(0, 50000) if not score else score

    msg = UpdatePlayerRequest(
        name=name,
        level=level,
        highscore=score,
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
    client,
    authtoken,
    playername: str,
    leaderboard_id: str,
    score: int,
    character: int,
    country: str,
    level: int,
):
    url = api_url + "/rpc/leaderboard.ext.v1.PrivateService/SubmitScore"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {authtoken}",
    }

    body = {
        "leaderboard": {
            "id": leaderboard_id,
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
    counter: int = 0,
    name: str = None,
    country: str = "us",
    leaderboard: str = "top_run_weekly_v2",
    score: str = "2147483647",
    level: int = 50,
    character: int = "-1534276928",
    surfer: int = None,
    avatar: str = None,
    player_score: int = None,
    player_level: int = None,
    lock=None,
):
    try:
        if not name:
            name = generate_name()

        auth = await auth_register(client)
        authtoken = auth["idToken"]

        await create_player(
            client,
            authtoken,
            name,
            surfer,
            avatar,
            player_score,
            player_level,
        )

        await send_scores(
            client,
            authtoken,
            name,
            leaderboard,
            score,
            character,
            country,
            level,
        )

        async with lock:
            counter["remaining"] -= 1
            if counter["remaining"] < 0:
                counter["remaining"] = 0
            print(f"\rRemaining: {counter['remaining']}", end="", flush=True)

    except Exception as e:
        print("Error:", e)


async def main_async(args):
    counter = {"remaining": args.amount}

    limits = httpx.Limits(max_connections=100, max_keepalive_connections=50)

    async with httpx.AsyncClient(http2=True, limits=limits, timeout=20) as client:

        levels = LEVELS if args.alllevel else [args.level]
        countries = COUNTRIES if args.allcountry else [args.country]

        if args.rickroll:
            names = [
                RICKROLL_NAMES[i % len(RICKROLL_NAMES)] for i in range(args.amount)
            ]
        else:
            names = [args.name] * args.amount

        lock = asyncio.Lock()

        tasks = [
            worker(
                client=client,
                counter=counter,
                name=name,
                country=country,
                leaderboard=args.leaderboard,
                score=args.score,
                level=level,
                character=args.character,
                avatar=args.avatar,
                player_score=args.playerscore,
                player_level=args.playerlevel,
                lock=lock,
            )
            for level in levels
            for country in countries
            for name in names
        ]

        await asyncio.gather(*tasks)


def main():
    countries = get_countrys()

    parser = argparse.ArgumentParser(description="Run TopRun spammer.")

    ex_name = parser.add_mutually_exclusive_group()

    ex_level = parser.add_mutually_exclusive_group()

    ex_name.add_argument("--rickroll", action="store_true", help="Enable Rickroll")

    ex_name.add_argument("-n", "--name", type=str, help="Name")

    parser.add_argument("-a", "--amount", default=100, type=int, help="Amount")
    ex_level.add_argument("--allcountry", action="store_true", help="All Countries")
    parser.add_argument(
        "-c",
        "--country",
        type=str,
        default="us",
        help="Country",
    )

    ex_level.add_argument(
        "-l",
        "--level",
        type=int,
        choices=LEVELS,
        default=LEVELS[-1],
        help="Level",
    )

    ex_level.add_argument("--alllevel", action="store_true", help="All Levels")

    parser.add_argument(
        "--leaderboard", type=str, default="top_run_weekly_v2", help="Leaderboard id"
    )

    parser.add_argument(
        "-s",
        "--score",
        type=int,
        default=2147483647,
        help="Toprun Score",
    )

    parser.add_argument(
        "--playerscore",
        type=int,
        default=2147483647,
        help="Player Score",
    )

    parser.add_argument(
        "--playerlevel",
        type=int,
        default=50,
        help="Player Level",
    )

    parser.add_argument(
        "--character",
        type=int,
        default=None,
        help="Player Character",
    )

    parser.add_argument(
        "--avatar",
        type=str,
        default="Avatar",
        help="Player Avatar",
    )

    args = parser.parse_args()

    if args.country.lower() not in [c["code"].lower() for c in countries]:
        print("Invalid country code")
        return

    if args.name:
        if not (1 <= len(args.name) <= 15) or not re.match(
            r"^[A-Za-z0-9]+$", args.name
        ):
            print("Name must be 1-15 characters and contain only letters or numbers")
            sys.exit(1)

    try:
        asyncio.run(main_async(args))
    except KeyboardInterrupt:
        print("Script terminated by user.")
        sys.exit(1)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
