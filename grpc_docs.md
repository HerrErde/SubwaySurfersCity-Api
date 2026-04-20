# Explanations

## Table of Contents

<details>
  <summary>Table of Contents</summary>
  
- [Explanations](#explanations)
  - [Table of Contents](#table-of-contents)
  - [General Notes](#general-notes)
  - [Identity File](#identity-file)
    - [Expired identityToken](#expired-identitytoken)
  - [Request body format](#request-body-format)
  - [Endpoints](#endpoints)
    - [Player](#player)
      - [Create Player](#create-player)
      - [Update Player](#update-player)
      - [Get Player](#get-player)
      - [Get Player by Tag](#get-player-by-tag)
      - [Get Player by Id](#get-player-by-id)
    - [Abtesting](#abtesting)
      - [MatchExperiments](#matchexperiments)
    - [Leaderboard](#leaderboard)
      - [Get Score](#get-score)
      - [Submit Score](#submit-score)

</details>

## General Notes

All knowledge is for versions `2.1.2`

> [!WARNING]
> Changes are expected to happen

grpc-status-details-bin content is base64

After registering an account, you'll have to create a player to use all the requests; otherwise, the account is 'empty' and can't perform player actions

All time values are in epoch time

this is a player tag `BY1BJH84CVHHIX` \
this is a player uid `0197351b-ae06-7a3f-8576-0e3d5b95a280`

Some response bodies that contain repeating data or with minor changes will be truncated to avoid repetition.

The default api url is `subwaycity.prod.sybo.net`

## Identity File

The identity file contains a dictionary with the user dict which contains id, name, picture, links list
and a refresh and identityToken dict that both contain a `token` value. \
A `expiresAt` value will tell the app when to refresh the token is expired.

All tokens are have 7 days ttl (time to live)

```json
{
  "user": {
    "id": "01968c3a-3fea-7abc-897c-e1a1814ba489",
    "name": null,
    "picture": null,
    "links": []
  },
  "refreshToken": {
    "token": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2OGMzYS0zZmVhLTdhYmMtODk3Yy1lMWExO..."
  },
  "identityToken": {
    "token": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2NzJiOS0yZThiLTc0NWEtOWQ1My1lMzg4MT...",
    "expiresAt": "2025-05-08T14:22:29.8031690Z"
  }
}
```

jwt (striped signatures)

Identity token

```json
{"alg":"PS256","typ":"JWT"}
{"sub":"019672b9-2e8b-745a-9d53-e3881534096c","iat":1745681460,"exp":1746286260}
```

refresh token

```json
{
  "sub": "01968c3a-3fea-7abc-897c-e1a1814ba489",
  "iat": 1746109349,
  "key": "44iuWfCHuem59orhD8RcZx4d6wmj2Zn3fvcpJ94lkFNqQfbrWequH364G8JUYfhN"
}
```

### Expired identityToken

When refreshing a identity token but still making requests with the old token, it will seem to work just fine, but e.g. your game (with the now new refreshed token) will have no changes (send invite will only appear on the player with the token, not the new one). \
Make sure to keep your identityToken refreshed and the everywhere the same.

## Request body format

You do not always need the `.proto` files or generated protobuf classes just to call an endpoint. The same request can be sent with a JSON body instead of a protobuf payload. When doing that, set the request header to `Content-Type: application/json` and structure the JSON so it matches the protobuf message layout as closely as possible.

For example, this protobuf-style request:

```python
msg = GetScoresRequest(
    leaderboard=LeaderboardInput(
        id="top_run_weekly_v2",
        partitions=PartitionsInput(
            partitionStrings=[PartitionString(key="cc", value="us")],
            partitionIntegers=[PartitionInteger(key="lvl", value=50)],
        ),
    )
)
```

can be represented as this JSON body:

```python
body = {
    "leaderboard": {
        "id": "top_run_weekly_v2",
        "partitions": {
            "partitionStrings": [
                {"key": "cc", "value": "us"}
            ],
            "partitionIntegers": [
                {"key": "lvl", "value": 50}
            ],
        },
    }
}
```

## Endpoints

### Player

<details id="player_response">
  <summary>Player</summary>

```protobuf
player {
  name: "StellarRat"
  tag: "XFKD9ZF6YV66MQ"
  level: 50
  highscore: 10145
  metadata {
    key: "HighScoreCharacterKey"
    value: "DataTag(-1836944478)"
  }
  metadata {
    key: "AvatarKey"
    value: "Avatar1"
  }
  created_at {
    seconds: 1772098927
    nanos: 365190000
  }
  update_player_at {
    seconds: 1772101114
    nanos: 732666000
  }
  uid: "0198836e-fb91-7900-9fa4-598349e4a77d"
}
```

</details>

#### Create Player

- POST `/rpc/player.ext.v1.PrivateService/CreatePlayer`
- Creates a Player into the account
- Sample request (2026-02-26): \
  POST /rpc/player.ext.v1.PrivateService/CreatePlayer \
  Authorization: `Bearer <identityToken>` \
  msg: CreatePlayerRequest \
  resp: CreatePlayerResponse

[Player fields](#player_fields)

#### Update Player

- POST `/rpc/player.ext.v1.PrivateService/UpdatePlayer`
- Updates the Player Profile
- Sample request (2026-02-26): \
  POST /rpc/player.ext.v1.PrivateService/UpdatePlayer \
  Authorization: `Bearer <identityToken>` \
  msg: UpdatePlayerRequest \
  resp: UpdatePlayerResponse

Update fields

<details id="player_fields">
  <Summary>Player fields</Summary>

<!-- prettier-ignore-start -->

| Id  | Type | Limit | Special |
| --- | ---- | ----- | ------- |
| name | string | 2-15 characters, only alphabet letters, no numeric | 604800 seconds (7 days) regex: `^[a-zA-Z]+$` |
| level | int | 0-50 |  |
| highscore | int | 0-2500000000 | |

<!-- prettier-ignore-end -->

</details>

#### Get Player

- POST `/rpc/player.ext.v1.PrivateService/GetPlayer`
- Gets the current player
- Sample request (2026-02-26): \
  POST /rpc/player.ext.v1.PrivateService/GetPlayer \
  Authorization: `Bearer <identityToken>` \
  msg: GetPlayerRequest \
  resp: GetPlayerResponse

This will get data of the own player \
It will return the [`Player`](#player_response) body.

The fields do not show up directly after generating the Player \
All metadata fields will not exist until they are set with UpdatePlayer

Additionally, the `updated_at`, `name_change_expires_at` and`name_changed_at` only show when the name is changed from the name the player was created with to a new one.

#### Get Player by Tag

- POST `/rpc/player.ext.v1.PrivateService/GetPlayerByTag`
- Gets the player by Tag
- Sample request (2026-02-26): \
  POST /rpc/player.ext.v1.PrivateService/GetPlayerByTag
  Authorization: `Bearer <identityToken>` \
  msg: GetPlayerByTagRequest \
  resp: GetPlayerByTagResponse

This gets a player by their invite Tag \
It will return the [`Player`](#player_response) body.

#### Get Player by Id

- POST `/rpc/player.ext.v1.PrivateService/GetPlayerById`
- Gets the player by id
- Sample request (2026-02-26): \
  POST /rpc/player.ext.v1.PrivateService/GetPlayerById \
  Authorization: `Bearer <identityToken>` \
  msg: GetPlayerByIdRequest \
  resp: GetPlayerByIdResponse

This gets a player by their uid \
It will return the [`Player`](#player_response) response body.

To get a player’s data, you first need their uid. This can be obtained either from their tag (invite ID) or, for your own account, from the auth/prod/identity file where it is stored in the id field.

### Abtesting

#### MatchExperiments

- POST `/rpc/abtesting.ext.v2.PrivateService/MatchExperiments`
- Returns the accounts experiment
- Sample request (2026-03-22): \
  POST /rpc/abtesting.ext.v2.PrivateService/MatchExperiments \
  Authorization: `Bearer <identityToken>`
  msg: MatchExperimentsRequest \
  resp: MatchExperimentsResponse

```protobuf
experiment {
  experimentId: "Tier1_AB_Interstitial_Frequency_2.1.0"
  variantId: "ab_interstitials_higher_frequency_xp_4"
}
```

<details>
  <summary>When requesting it with application/json</summary>

```json
{
  "experiments": [
    {
      "experimentId": "ab_reduced_max_tickets_2.1.0",
      "variantId": "ab_ticketing_variant_b",
      "variantType": "VARIANT_TYPE_GAMEDATA",
      "endAt": "2126-04-01T08:04:15.544Z"
    }
  ]
}
```

</details>

When you want to play with other experiments you can change them [here](./hacks.md#play-with-experiments). \
The app uses this information to determine which tower gamedata files to load.

The weird thing is that when requesting the json format it will output the `variantType` and `endAt` values, which it dosnt when doing the normal grpc request.

### Leaderboard

#### Get Score

- POST `/rpc/leaderboard.ext.v1.PrivateService/GetScores`
- Get the TopRun Leaderboard
- Sample request (2026-02-26): \
  POST /rpc/leaderboard.ext.v1.PrivateService/GetScores \
  Authorization: `Bearer <identityToken>`
  msg: GetPlayerByIdRequest \
  resp: GetPlayerByTagResponse

<details>
  <summary>When requesting it with application/json</summary>

```json
{
  "leaderboard": {
    "id": "top_run_weekly_v2",
    "partitions": {
      "partitionStrings": [
        {
          "key": "cc",
          "value": "us"
        }
      ],
      "partitionIntegers": [
        {
          "key": "lvl",
          "value": 50
        }
      ]
    }
  }
}
```

</details>

<details id="leaderboard_response">
  <summary>Leaderboard</summary>

```json
{
  "leaderboard": {
    "id": "top_run_weekly_v2",
    "partitions": {
      "partitionStrings": [{ "key": "cc", "value": "us" }],
      "partitionRanges": [{ "key": "lvl", "min": 41, "max": 2147483647 }]
    },
    "resetsAt": "2026-03-02T09:00:00Z",
    "scoreCount": "100"
  },
  "score": {
    "uid": "",
    "rank": "0",
    "value": "0",
    "metadata": [],
    "player": null
  },
  "scores": [
    {
      "uid": "019c8e47-dd05-7e20-a9b6-f139a6a73da5",
      "rank": "1",
      "value": "2147470008",
      "metadata": [
        { "key": "playerName", "value": "Player73da5" },
        { "key": "characterName", "value": "299562833" }
      ],
      "player": {
        "uid": "019c8e47-dd05-7e20-a9b6-f139a6a73da5",
        "name": "momo",
        "tag": "GBMWPXASCQIMXU",
        "level": 50,
        "highscore": "2147470008",
        "metadata": {
          "AvatarKey": "Avatar10",
          "HighScoreCharacterKey": "DataTag(299562833)"
        },
        "createdAt": "2026-02-24T06:19:53.805151Z",
        "updatedAt": "2026-02-24T07:22:32.462032Z",
        "renamedAt": "2026-02-24T07:22:32.412489Z",
        "renameableAt": "2026-03-03T07:22:32.412489Z"
      }
    },
    {
      "uid": "019c9757-14cc-74d1-ad4c-6698dc6473b3",
      "rank": "2",
      "value": "2147453657",
      "metadata": [
        { "key": "playerName", "value": "Player473b3" },
        { "key": "characterName", "value": "299562833" }
      ],
      "player": {
        "uid": "019c9757-14cc-74d1-ad4c-6698dc6473b3",
        "name": "Muhamed",
        "tag": "CEBIMF7YN5LWZE",
        "level": 50,
        "highscore": "2147453657",
        "metadata": {
          "AvatarKey": "Avatar14",
          "HighScoreCharacterKey": "DataTag(299562833)"
        },
        "createdAt": "2026-02-26T00:31:21.420752Z",
        "updatedAt": "2026-02-26T01:32:13.103517Z",
        "renamedAt": "2026-02-26T00:50:01.398659Z",
        "renameableAt": "2026-03-05T00:50:01.398659Z"
      }
    }
    truncated 99x
  ]
}
```

</details>

#### Submit Score

- POST `/rpc/leaderboard.ext.v1.PrivateService/SubmitScore`
- Submit Run score
- Sample request (2026-02-26): \
   POST /rpc/leaderboard.ext.v1.PrivateService/SubmitScore \
   Authorization: `Bearer <identityToken>` \
   msg: GetPlayerByIdRequest \
   resp: GetPlayerByTagResponse

<details>
  <summary>When requesting it with application/json</summary>

```json
{
  "leaderboard": {
    "id": "top_run_weekly_v2",
    "partitions": {
      "partitionStrings": [
        {
          "key": "cc",
          "value": "us"
        }
      ],
      "partitionIntegers": [
        {
          "key": "lvl",
          "value": 50
        }
      ]
    }
  },
  "score": {
    "value": "7977",
    "metadata": [
      {
        "key": "playerName",
        "value": "StellarRat"
      },
      {
        "key": "characterName",
        "value": "-1836944478"
      }
    ]
  }
}
```

</details>

Response: [TopRun Leaderboard](#leaderboard_response)
