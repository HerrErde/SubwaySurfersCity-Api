import httpx

from featureflags_pb2 import *
from utils import *


def get_flags():
    url = api_url + "/rpc/featureflags.ext.v1.PublicService/GetFlags"

    msg = GetFlagsRequest(clientVersion=Version(major=2, minor=2, patch=0))

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
        resp = GetFlagsResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())
        print("No valid response received.")


get_flags()
