import httpx

from utils import *
from leaderboard_pb2 import *


def get_scores():
    url = api_url + "/rpc/leaderboard.ext.v1.PrivateService/GetScores"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {identityToken}",
    }

    body = {
        "leaderboard": {
            "id": "top_run_weekly_v2",
            "partitions": {
                "partitionStrings": [{"key": "cc", "value": "us"}],
                "partitionIntegers": [{"key": "lvl", "value": 50}],
            },
        }
    }

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            json=body,
        )

    try:
        print(r.json())
    except Exception as e:
        print("Failed to get response:", e)


def get_scores_proto():
    url = api_url + "/rpc/leaderboard.ext.v1.PrivateService/GetScores"

    msg = GetScoresRequest(
        leaderboard=LeaderboardInput(
            id="top_run_weekly_v2",
            partitions=PartitionsInput(
                partitionStrings=[PartitionString(key="cc", value="us")],
                partitionIntegers=[PartitionInteger(key="lvl", value=50)],
            ),
        )
    )

    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    raw = r.content
    print(raw)
    if len(raw) < 5:
        print("Response too short")
        return

    grpc_payload = deframing(raw)

    try:
        resp = GetPlayerByTagResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())
        print("No valid response received.")


def send_scores(playername: str, score: int, character: int):
    url = api_url + "/rpc/leaderboard.ext.v1.PrivateService/SubmitScore"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {identityToken}",
    }

    body = {
        "leaderboard": {
            "id": "top_run_weekly_v2",
            "partitions": {
                "partitionStrings": [{"key": "cc", "value": "us"}],
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

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            json=body,
        )

    try:
        print(r.json())
    except Exception as e:
        print("Failed to get response:", e)


def send_scores_proto(playername: str, score: int, character: int):
    url = api_url + "/rpc/leaderboard.ext.v1.PrivateService/SubmitScore"

    msg = SubmitScoreRequest(
        leaderboard=LeaderboardInput(
            id="top_run_weekly_v2",
            partitions=PartitionsInput(
                partitionStrings=[PartitionString(key="cc", value="us")],
                partitionIntegers=[PartitionInteger(key="lvl", value=50)],
            ),
        ),
        score=ScoreInput(
            value=str(score),
            metadata=[
                MetadataEntry(key="playerName", value=playername),
                MetadataEntry(key="characterName", value=str(character)),
            ],
        ),
    )

    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    raw = r.content
    print(raw)
    if len(raw) < 5:
        print("Response too short")
        return

    grpc_payload = deframing(raw)

    try:
        resp = SubmitScoreResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())
        print("No valid response received.")


get_scores()
get_scores_proto()
# send_scores()
