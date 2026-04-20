> [!WARNING]  
> This project is intended strictly for educational and research purposes only.  
> The author assumes no responsibility for any consequences arising from the use of this tool, including but not limited to account bans or data loss.  
> Use it at your own risk.
> Follow the [SYBO TOS](https://sybogames.com/terms-of-service) or whatever

# SubwayCity API

You can interact with the internal api that is used by the [Subway City](https://play.google.com/store/apps/details?id=com.sybogames.subway.surfers.game) game app.

You can also checkout the [Subway Surfers API](https://github.com/HerrErde/SubwaySurfers-API)

---

[RPC Docs](./grpc_docs.md) \
[Json Docs](./json_docs.md)

## Requirements

- `grpcio` and `protobuf` Python packages installed
- Protocol Buffers Compiler (`protoc`) installed and accessible via command line

## Setup and Usage

```bash
pip install -r requirements.txt
cd send
protoc -I=protos --python_out=. protos\*.proto
python -m grpc_tools.protoc -I=protos --python_out=. --grpc_python_out=. protos\*.proto
```

```bash
python player.py
python abtesting.py
python leaderboard.py
python sendjson.py
```

## How to Use

### 1. Register a New Account (Optional)

- Run the script:

  ```bash
  python send/auth.py
  ```

- This will generate two tokens:
  - `identityToken`
  - `refreshToken`

  - Or you can request the endpoints manually

  - The easiest way is to use it with a .env file and the variable `IDENTITYTOKEN`

### 2. Create a Player (Only if You Registered a New Account)

- After registering, you must create a player profile before you can use most API endpoints. (not needed when using `auth.py`)

### 3. Obtain Your `identityToken`

- **If you already have a Subway Surfers City account:**
  1. Open the `auth/prod/identity` file inside your game directory.
  2. The file is JSON formatted. Copy the value of `"identityToken"`.

- **If you registered a new account:**
  Use the `identityToken` returned by `python send/auth.py`.

### Token Refresh

- A `identityToken` is valid for **7 days**.
- Use your `refreshToken` to request a new `identityToken` when it expires.
- Always replace the old token everywhere you use it.

## API Documentation

- [RPC Docs](./grpc_docs.md) – gRPC endpoints, request/response formats, examples
- [JSON Docs](./json_docs.md) – JSON endpoints, request/response formats, examples

---

> **Note:** Always use a valid `identityToken` in your requests.
> **Tip:** Refresh your token regularly and update it wherever it’s used.

### Development

If you want to decode the requests yourself, root your phone, use an emulator, or patch the app.

Then use **PCAPdroid** to capture traffic and export it as a PCAP file. Open the file in **Wireshark**, locate the gRPC request (filter by searching "gprc"), and inspect the **Protocol Buffer** section. From there, copy the `value` inside the relevant `Field()`. Then you can decode a the Protobuf, in somehing like [protobuf-decoder](https://good.tools/protobuf-decoder). The same can be done with the response.
