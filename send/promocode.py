import httpx

from promocodes_pb2 import *
from utils import *


def redeem_code():
    url = api_url + "/rpc/promocodes.ext.v1.PrivateService/RedeemCode"

    msg = RedeemCodeRequest(id="TESTCODE", platform=Platform.Google, version="2.2.0")

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
        resp = RedeemCodeResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())
        print("No valid response received.")


redeem_code()
