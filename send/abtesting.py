import httpx

from abtesting_pb2 import *
from utils import *


def get_abtesting():
    url = api_url + "/rpc/abtesting.ext.v2.PrivateService/MatchExperiments"

    msg = MatchExperimentsRequest(
        metrics={
            "language": "en",
            "age": "34",
            "platform": "android",
            "coppa": "false",
            "gameVersion": "2.1.0",
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
    elif r.content:
        if "text/html" in r.headers.get("Content-Type"):
            print("Content is html")
            return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = MatchExperimentsResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
        print("gRPC payload (hex):", grpc_payload.hex())


get_abtesting()
