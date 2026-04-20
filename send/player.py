import httpx

from player_pb2 import *
from utils import *


def get_player_by_tag(playertag: str):
    url = api_url + "/rpc/player.ext.v1.PrivateService/GetPlayerByTag"

    msg = GetPlayerByTagRequest(
        tag=playertag,
    )
    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    raw = r.content
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


def get_player_by_id(playeruuid: str):
    url = api_url + "/rpc/player.ext.v1.PrivateService/GetPlayerById"

    msg = GetPlayerByIdRequest(
        uid=playeruuid,
    )

    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    raw = r.content
    if len(raw) < 5:
        print("Response too short")
        return

    grpc_payload = deframing(raw)

    try:
        resp = GetPlayerByIdResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())
        print("No valid response received.")


def get_player():
    url = api_url + "/rpc/player.ext.v1.PrivateService/GetPlayer"

    msg = GetPlayerRequest()

    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    raw = r.content
    if len(raw) < 5:
        print("Response too short")
        return

    grpc_payload = deframing(raw)

    try:
        resp = GetPlayerResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
        # print("payload bytes:", resp.SerializeToString())
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def create_player():
    url = api_url + "/rpc/player.ext.v1.PrivateService/CreatePlayer"

    msg = CreatePlayerRequest(
        name="CoolNiko",
        level=50,
        highscore=1000,
        metadata={
            "HighScoreCharacterKey": "DataTag(-1836944478)",
            "AvatarKey": "Avatar1",
        },
    )

    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    raw = r.content

    if len(raw) < 5:
        print("Response too short")
        return

    grpc_payload = deframing(raw)

    try:
        resp = CreatePlayerResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())
        print("No valid response received.")


def update_player():
    from player_pb2 import PlayerResponse, UpdatePlayerRequest

    url = api_url + "/rpc/player.ext.v1.PrivateService/UpdatePlayer"

    msg = UpdatePlayerRequest(
        name="StellarRat",
        level=50,
        highscore=12878488,
        metadata={
            "HighScoreCharacterKey": "DataTag(-1505268145)",
            "AvatarKey": "Avatar13",
        },
    )

    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    print(statusmessage(r))

    raw = r.content

    if len(raw) < 5:
        print("Response too short")
        return

    grpc_payload = deframing(raw)

    try:
        resp = UpdatePlayerResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def get_config():
    url = api_url + "/rpc/player.ext.v1.PrivateService/GetConfig"

    msg = GetConfigRequest()

    body = framing(msg)

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    raw = r.content
    if len(raw) < 5:
        print("Response too short")
        return
    elif r.content:
        if "text/html" in r.headers.get("Content-Type"):
            print("Content is html")
            return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = GetConfigResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
        print("gRPC payload (hex):", grpc_payload.hex())


# create_player()
# update_player()
# get_player()
# get_player_by_tag("XFKD9ZF6YV66MQ")
# get_player_by_id("0198836e-fb91-7900-9fa4-598349e4a77d")
# get_config()
