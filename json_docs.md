# Explanations

## Table of Contents

<details>
  <summary>Table of Contents</summary>

- [Explanations](#explanations)
  - [Table of Contents](#table-of-contents)
  - [General Notes](#general-notes)
    - [Auth](#auth)
      - [Register](#register)
      - [Refresh](#refresh)
      - [Play Connect](#play-connect)
      - [Play Login](#play-login)
    - [Content](#content)
      - [Manifest](#manifest)
      - [Gamedata](#gamedata)
      - [Assets](#assets)
      - [Assets V2](#assets-v2)
    - [GDPR](#gdpr)
      - [GDPR delete](#gdpr-delete)
      - [GDPR status](#gdpr-status)
    - [Profile](#profile)
      - [Get Profile](#get-profile)
      - [Send Profile](#send-profile)
    - [Mail](#mail)
      - [Get](#get)
      - [Read](#read)
    - [Misc](#misc)
      - [Where](#where)
      - [When](#when)
    - [Shop](#shop)

</details>

## General Notes

All knowledge is for versions `2.1.2`

> [!WARNING]
> Changes are expected to happen

After registering an account, you'll have to create a player to use all the requests; otherwise, the account is 'empty' and can't perform player actions.

this is a player tag `BY1BJH84CVHHIX` \
this is a player uuid `0197351b-ae06-7a3f-8576-0e3d5b95a280`

Some response bodies that contain repeating data or with minor changes will be truncated to avoid repetition.

The default api url is `subwaycity.prod.sybo.net`

### Auth

#### Register

- POST `/v2.0/auth/register`
- Will register a player account
- Sample request (2026-02-26): \
  POST /v2.0/auth/register

- Sample response:

  ```json
  {
    "idToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2OGMzYS0zZmVhLTdhYmMtODk3Yy1lMWExO...",
    "idTokenTtl": 604800,
    "refreshToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2NzJiOS0yZThiLTc0NWEtOWQ1My1lMzg4MT...",
    "user": { "id": "01968c3a-3fea-7abc-897c-e1a1814ba489", "links": [] }
  }
  ```

This creates an empty account and returns an identity token and a refresh token. \
It generates a idenity and a refresh token, with a ttl (time to live). \
The account itself does not yet have a player profile. To initialize the player, you must send a request to [CreatePlayer](./grpc_docs.md#create-player) with data. \
Only after creating the player, other game-related requests, such as [UpdatePlayer](./grpc_docs.md#update-player), be used.

#### Refresh

- POST `/v2.0/auth/refresh`
- Refresh the accounts identity token
- Sample request (2026-02-26): \
  POST /v2.0/auth/refresh

  Body:

  ```json
  {
    "refreshToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2NzJiOS0yZThiLTc0NWEtOWQ1My1lMzg4MT...",
    "fbAccessToken": null
  }
  ```

- Sample response:

  ```json
  {
    "idToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2OGMzYS0zZmVhLTdhYmMtODk3Yy1lMWExO...",
    "idTokenTtl": 604800,
    "refreshToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMTk2NzJiOS0yZThiLTc0NWEtOWQ1My1lMzg4MT...",
    "user": { "id": "01968c3a-3fea-7abc-897c-e1a1814ba489", "links": [] }
  }
  ```

This refreshes the accounts identity token and returns a new token, allowing the account to continue making authenticated requests.

#### Play Connect

- POST `/v1.0/auth/play/connect`
- Play connect
- Sample request (2026-02-26): \
  POST /v1.0/auth/play/connect \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  {
    "authcode": "4/0AfrIepArxA2nQmU1-..."
  }
  ```

<h5>Default Response</h5>

```json
{
  "idToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9...",
  "idTokenTtl": 604800,
  "refreshToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9..",
  "user": {
    "id": "0198836e-fb91-7900-9fa4-598349e4a77d",
    "links": [{ "type": "play", "id": "a_2520406209192914419" }]
  }
}
```

<h5>Error Response</h5>

```json
{ "error": "request failed", "kind": 6 }
```

#### Play Login

- POST `/v1.0/auth/play/login`
- Play login
- Sample request (2026-02-26): \
  POST /v1.0/auth/play/login \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  {
    "authcode": "4/0AfrIepDPZf2gwn0pDNzTbSYhKr8twvlo-a9U-9jVP7TPS-qoj_0jDmrlJyDQbFNUkzGH7Q"
  }
  ```

<h5>Default Response</h5>

```json
{
  "idToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9...",
  "idTokenTtl": 604800,
  "refreshToken": "eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9..",
  "user": {
    "id": "0198836e-fb91-7900-9fa4-598349e4a77d",
    "links": [{ "type": "play", "id": "a_2520406209192914419" }]
  }
}
```

### Content

#### Manifest

Url is <https://manifest.tower.sybo.net>

- GET `/v1.0/{game}/{version}/{type}/{secret}/{experiment}/manifest.json`
- Gets the manifest of a game version
- Sample request (2025-12-20): \
  GET /v1.0/{game}/{version}/{type}/{secret}/{experiment}/manifest.json

<details>
  <summary>Android development</summary>

```json
{
  "secret": "c1f28cce71240cb3bfff9b",
  "game": "subwaycity",
  "platform": "android",
  "version": "2.0.4",
  "lifecycle": "development",
  "addressables": null,
  "services": {
    "meta-dev": "https://subwaycity.dev.sybo.net",
    "meta-prod": "https://subwaycity.prod.sybo.net",
    "meta-stage": "https://subwaycity.stage.sybo.net"
  },
  "metadata": {
    "privacy_url": "https://sybogames.com/privacy-policy",
    "store_url": "market://details?id=com.sybogames.subway.surfers.game",
    "terms_url": "https://sybogames.com/terms-of-service"
  },
  "gamedata": "042cd4efa1ed894c34e752e59fa7b99b53e80c8e"
}
```

</details>
<details>
  <summary>Apple retired</summary>

```json
{
  "secret": "2b45ed265fd136000f221f",
  "game": "subwaycity",
  "platform": "ios",
  "version": "1.29.0",
  "lifecycle": "retired",
  "addressables": null,
  "services": {
    "meta-dev": "https://subwaycity.dev.sybo.net",
    "meta-prod": "https://subwaycity.prod.sybo.net",
    "meta-stage": "https://subwaycity.stage.sybo.net"
  },
  "metadata": {
    "privacy_url": "https://sybogames.com/privacy-policy",
    "store_url": "itms-apps://itunes.apple.com/app/id6504188939",
    "terms_url": "https://sybogames.com/terms-of-service"
  },
  "gamedata": "bf46a54b0f4539c6b892d391755abb28e050938a"
}
```

</details>

<br>

Notes: \
 From this data you get the version specific manifest data. \
 Which gives useful data like gamedata hash and lifecycle. \
 You get the secret by extracting it from the game file (apk or ipa). \
 The `assets/settings/sybo.tower.default.json` (ipa is `Payload/SubwaySurf.app/Data/Raw/settings/sybo.tower.default.json`) file contains a key called `Secret`, with the version specific secret.

**Url examples**

```
https://manifest.tower.sybo.net/v1.0/subwaycity/2.0.4/android/c1f28cce71240cb3bfff9b/manifest.json
https://manifest.tower.sybo.net/v1.0/subwaycity/1.29.0/android/2b45ed265fd136000f221f/manifest.json
https://manifest.tower.sybo.net/v1.0/subway/3.44.2/android/s8B88pVbhzpKmvX6BV0u/ab_revive_codechange/manifest.json
```

_Default Schema_

```
https://manifest.tower.sybo.net/v1.0/{game}/{version}/{platform}/{secret}/manifest.json
```

_Experiment Schema_

```
https://manifest.tower.sybo.net/v1.0/{game}/{version}/{platform}/{secret}/{experiment}/manifest.json
```

- GET `/v2.0/{game}/{version}/{type}/{secret}/{experiment}/archive.zip`
- Get the manifest of a game version
- Sample request (2025-12-20): \
  GET /v2.0/{game}/{version}/{type}/{secret}/{experiment}/archive.zip

When using the v2.0 schema, you can use the `archive.zip` endpoint to get a zip file of the game files. \
It seems like the v2.0 schema only has the `archive` endpoint, all other do not exist.

```
https://manifest.tower.sybo.net/v2.0/subwaycity/2.0.4/android/c1f28cce71240cb3bfff9b/archive.zip
```

The archive.zip contains the manifest.json aswell as a `data` folder with the gamedata files.

```
manifest.json
data/
   surfers.json
   boards.json
   ...
```

#### Gamedata

You can get the gamedata/tower files in bypass of the old depreciated method of extracting the apk gamefile or ipa gamefile (ipa still works), using from the manifest request contained `gamedata` hash value
(state 2.0.4)

You can request the `manifest.json`, which contains the manifest of all the existing files in gamedata.

```json
{
  "experiment": "default",
  "game": "subwaycity",
  "objects": {
    "anrMonitor": {
      "filename": "anrMonitor.json",
      "key": "c883382089f22a80fac34d618d0b31b6ffe0fb56"
    },
    "boards": {
      "filename": "boards.json",
      "key": "112ac7c80b4ae7015f8ec3644c71998a144561b7"
    },
    "bonusReward": {
      "filename": "bonusReward.json",
      "key": "ad36fa47bfdc1020e5c23e7141b768ca714fc6b1"
    }
    (truncated)
  },
  "spec": "v1.0",
  "version": "2.0.2"
}
```

```
https://gamedata.tower.sybo.net/v1.0/subwaycity/042cd4efa1ed894c34e752e59fa7b99b53e80c8e/manifest.json
```

```
https://gamedata.tower.sybo.net/v1.0/{game}/{gamedataSecret}/{filename}.json
```

#### Assets

Url <https://assets.tower.sybo.net>

- GET `/`
- Get game assets files
- Sample request (2025-12-20): \
  GET /

When getting the root of the url it shows what seems to be a list of a bucket
> As of checking 2026-06-09 it will return a 403 error
>```xml
><Error>
><Code>AccessDenied</Code>
><Message>Access denied.</Message>
></Error>
>```



<details>
  <summary>Assets Response</summary>

```xml
<ListBucketResult>
<Name>sybogames-tower-assets</Name>
<Prefix/>
<Marker/>
<NextMarker>
v1.0/BRIM/20b6aac8-db25-45b7-b2e7-35efdf27a83d/catalog/1.0.0/catalog_2024.02.27.05.56.51.hash
</NextMarker>
<IsTruncated>true</IsTruncated>
<Contents>
<Key>
v1.0.0/ReleaseTesterApp/08ad4fa1-1fb6-4a8c-a782-de8c725f3e5e/addressable_data
</Key>
<Generation>1672672180447593</Generation>
<MetaGeneration>1</MetaGeneration>
<LastModified>2023-01-02T15:09:40.478Z</LastModified>
<ETag>"d41d8cd98f00b204e9800998ecf8427e"</ETag>
<Size>0</Size>
</Contents>
...
<Contents>
<Key>
v1.0/Atlas/a820cd4f-b422-4e04-8c46-b19db72f0b99/catalog/1.0.0/catalog_2021.11.25.10.14.22.json
</Key>
<Generation>1637836239952983</Generation>
<MetaGeneration>1</MetaGeneration>
<LastModified>2021-11-25T10:30:39.996Z</LastModified>
<ETag>"893cf305a3c4046801ffb92dc866f35d"</ETag>
<Size>9017</Size>
</Contents>
...
<Contents>
<Key>
v1.0/BRIM/0004b3b2-328d-40a6-8d5c-cdb07dbfa7bc/catalog/1.0.0/catalog_2023.11.15.10.18.13.hash
</Key>
<Generation>1700044260436100</Generation>
<MetaGeneration>1</MetaGeneration>
<LastModified>2023-11-15T10:31:00.468Z</LastModified>
<ETag>"fb9d3d1895d092d22581315f15d39373"</ETag>
<Size>32</Size>
</Contents>
```

</details>

<br>

- GET `v1.0/{game}/{bundleId}/{type}/{version}/{file}`
- Get game assets files
- Sample request (2025-12-20): \
  GET v1.0/{game}/{bundleId}/{type}/{version}/{file}

```
https://assets.tower.sybo.net/v1.0/subwaycity/4519c123-6cb5-482d-a907-6b92da4e16f9/bundle/1.0.0/sybo.subway2.art.surfers.jake_skin01_tier1_redblack_assets_all_1f584e81471de4a357883342cd63b0ee.bundle
```

This request will return the asset in the UnityFs format

Inside the apk (`assets/aa/catalog.json`) or ios (`Payload/SubwaySurf.app/Data/Raw/aa/catalog.json`) `catalog.json` file, the `m_InternalIds` list contains all file entries. These are links starting with `sybo://`, such as:

```
sybo://subwaycity/4519c123-6cb5-482d-a907-6b92da4e16f9/1.0.0/sybo.subway2.art.surfers.jake_skin01_tier1_redblack_assets_all_1f584e81471de4a357883342cd63b0ee.bundle
```

These entries reference the actual asset bundles used by the game.

#### Assets V2

Url <https://assets-v2.tower.sybo.net>

- Get game assets files
- Sample request (2026-06-09)

It seems to be just a new assets endpoint with seemingly no signifficant changes to [Assets](#assets).

### GDPR

#### GDPR delete

- POST `/v1.0/gdpr/delete`
- Requests a deletion
- Sample request (2026-02-26): \
  POST /v1.0/gdpr/delete \
  Authorization: `Bearer <identityToken>`

- Sample response:

  ```json
  {
    "job": {
      "kind": 1,
      "state": 0,
      "url": "",
      "createdAt": "2025-12-10T18:02:01.581790628Z",
      "endetAt": null
    }
  }
  ```

This is the account deletion request that will delete your account.

It only deletes your public profile (that was is shown when other players look at your player) not your save data \
when you are friends with a player you are removed from their friends list

it will only delete your `player` but not your `account`, that means you can just use `CreatePlayer` request again without the need of registering again.

#### GDPR status

- GET `/v1.0/gdpr/status`
- Get the status of the player deletion
- Sample request (2026-02-26): \
  GET /v1.0/gdpr/status \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  { "gaid": "00000000-0000-0000-0000-000000000000" }
  ```

- Sample response:

  ```json
  {
    "job": {
      "kind": 1,
      "state": 1,
      "url": "",
      "createdAt": "2025-12-10T18:02:01.581790628Z",
      "endetAt": "2025-12-10T18:02:02.566636Z"
    }
  }
  ```

This is the account delete status request, with wich you get the status of the current account delete request.

### Profile

**truncated version with several keys removed**

<details>
  <summary>Escaped Profile</summary>

```json
{
  "profile": "{\"runs\":5,\"trialRuns\":2,\"campaignRuns\":0,\"character\":1900660162,\"district\":-48406815,\"districtRecentUnlock\":0,\"tutorialStep\":5,\"stompedTimes\":9,\"tarpBouncedTimes\":9,\"bubbleBouncedTimes\":4,\"boardActivatedTimes\":8,\"onlinePlayerProfile\":{\"name\":\"StellarRat\",\"renameableAt\":\"0001-01-01T00:00:00\",\"tag\":\"XFKD9ZF6YV66MQ\",\"avatar\":\"Avatar5\"},\"surferLaddersClaimed\":[],\"playerLadderClaimed\":null,\"trialLadderClaimed\":null,\"unlocksSeen\":[],\"surferProfiles\":[{\"id\":-1836944478,\"level\":20,\"isUnlocked\":true,\"wasSeen\":true,\"highScore\":0,\"selectedSkin\":213457242},{\"id\":1900660162,\"level\":20,\"isUnlocked\":true,\"wasSeen\":true,\"highScore\":0,\"selectedSkin\":0},{\"id\":2129411796,\"level\":20,\"isUnlocked\":true,\"wasSeen\":true,\"highScore\":0,\"selectedSkin\":0},{\"id\":1614866432,\"level\":20,\"isUnlocked\":true,\"wasSeen\":true,\"highScore\":0,\"selectedSkin\":0},{\"id\":1804257387,\"level\":20,\"isUnlocked\":true,\"wasSeen\":true,\"highScore\":0,\"selectedSkin\":0},{\"id\":1663244716,\"level\":20,\"isUnlocked\":true,\"wasSeen\":true,\"highScore\":0,\"selectedSkin\":0},{\"id\":849273384,\"level\":20,\"isUnlocked\":true,\"wasSeen\":true,\"highScore\":0,\"selectedSkin\":0},{\"id\":1200047034,\"level\":20,\"isUnlocked\":true,\"wasSeen\":true,\"highScore\":0,\"selectedSkin\":0},{\"id\":1120354844,\"level\":20,\"isUnlocked\":true,\"wasSeen\":true,\"highScore\":0,\"selectedSkin\":0},{\"id\":581326566,\"level\":20,\"isUnlocked\":true,\"wasSeen\":true,\"highScore\":0,\"selectedSkin\":0},{\"id\":-1505268145,\"level\":20,\"isUnlocked\":true,\"wasSeen\":true,\"highScore\":0,\"selectedSkin\":0},{\"id\":299562833,\"level\":20,\"isUnlocked\":true,\"wasSeen\":true,\"highScore\":0,\"selectedSkin\":0}],\"wallet\":[{\"dataTag\":-1085419483,\"count\":999999},{\"dataTag\":1669706535,\"count\":10},{\"dataTag\":-1878560402,\"count\":120},{\"dataTag\":-1509662453,\"count\":4},{\"dataTag\":-633437229,\"count\":999999999},{\"dataTag\":722065917,\"count\":24},{\"dataTag\":543173782,\"count\":0},{\"dataTag\":449284577,\"count\":0},{\"dataTag\":-802311392,\"count\":0},{\"dataTag\":596132505,\"count\":0},{\"dataTag\":-116637823,\"count\":0},{\"dataTag\":1022801224,\"count\":0},{\"dataTag\":-156646249,\"count\":0},{\"dataTag\":-1806416624,\"count\":0},{\"dataTag\":-402320829,\"count\":9},{\"dataTag\":-1324639484,\"count\":0}],\"timestamps\":[{\"Id\":\"DailyMissionLastResetTimeStamp\",\"Ticks\":1772720716},{\"Id\":\"DailyMissionNextResetDateTime\",\"Ticks\":639083844000000000},{\"Id\":\"sch-campaign-weekly-campaign-speedpad-1\",\"Ticks\":639076945242920000},{\"Id\":\"Trials_IntroductionStartDate\",\"Ticks\":639076965667540000},{\"Id\":\"DailyMissionLastResetSeen\",\"Ticks\":639083844000000000},{\"Id\":\"sch-campaign-weekly-campaign-speedpad-2\",\"Ticks\":639083175346840000}],\"crew\":[{\"SurferId\":2129411796},{\"SurferId\":-1836944478},{\"SurferId\":1614866432}],\"goals\":[],\"quest\":[{\"QuestID\":\"trophy-thursday\",\"AnalyticID\":\"trophy-thursday_0e26ddb0-99e6-40f9-9a3d-c4be7c7ad99d\",\"Amount\":0,\"TimerID\":1338442653,\"ActiveStepIndex\":0,\"SavableItems\":[],\"PendingProgress\":0},{\"QuestID\":\"mega-coin-hunt\",\"AnalyticID\":\"mega-coin-hunt_a95c7281-3bba-401b-8fcc-f83491fba92c\",\"Amount\":0,\"TimerID\":942104232,\"ActiveStepIndex\":0,\"SavableItems\":[{\"Kind\":\"DataTag\",\"Tag\":852717139},{\"Kind\":\"DataTag\",\"Tag\":-1836944478},{\"Kind\":\"DataTag\",\"Tag\":299562833},{\"Kind\":\"DataTag\",\"Tag\":2129411796}],\"PendingProgress\":0}],\"questTriggered\":[{\"QuestID\":\"trophy-thursday\",\"TimeTriggered\":\"2026-03-05T14:25:16.0760000Z\"},{\"QuestID\":\"mega-coin-hunt\",\"TimeTriggered\":\"2026-03-05T14:25:16.0790000Z\"}],\"lifetimeReviveCount\":3}",
  "hash": "9b4b702d49f6e26e6677cb1e4aa567fd68323f46",
  "updated": "2026-03-05T14:59:47.099903Z",
  "version": 3
}
```

</details>

#### Get Profile

- GET `/v1.0/profile`
- Returns the current player's profile files
- Sample request (2026-02-26): \
  GET /v1.0/profile \
  Authorization: `Bearer <identityToken>`
- Sample response:

  ```json
  {
    "profile": "{\"runs\":5,\"trialRuns\":2,\"campaignRuns\":0,...",
    "hash": "9b4b702d49f6e26e6677cb1e4aa567fd68323f46",
    "updated": "2026-03-05T14:59:47.099903Z",
    "version": 3
  }
  ```

Returns the current player's profile files

When the player has never received profile data, it will return with a 404 error.

<h5>No profile data</h5>

```json
{
  "error": "request failed",
  "kind": 5
}
```

#### Send Profile

- POST /v2.0/profile
- Send the current player's profile save files
- Request (2026-02-26): \
   POST /v2.0/profile \
   Authorization: `Bearer <identityToken>` \
   Body:

  ```json
  {
    "profile": "{\"runs\":0,\"trialRuns\":0,\"campaignRuns\":0,...}",
    "version": 3
  }
  ```

- Sample response:

  ```json
  { "hash": "f4aada91994d684428cd681b049ccd4cb81f1f7f" }
  ```

Notes:

- With this request you can send your escaped JSON save files. \
  The `profile` data and `version` number can be almost any values and will be accepted by the server. \
  Valid version range: -999999999 — 999999999. Values outside this range return HTTP 400. \
  The `profile` field may contain any amount of data; sending an empty string for `profile` results in a 500 error.

Request example:

```json
{
  "profile": "",
  "version": 2
}
```

<h5>Default Response</h5>

```json
{
  "hash": "4d2bd1660d5428daf513c8339ee5e1a7bfabf12b"
}
```

### Mail

#### Get

- POST `/v2.0/mail`
- Gets a Announcement
- Sample request (2026-02-26): \
  POST /v2.0/mail \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  {
    "language": "en",
    "metrics": {
      "age": "47",
      "language": "en",
      "platform": "android",
      "coppa": "false",
      "gameVersion": "2.0.3"
    }
  }
  ```

<h5>Default Response</h5>

```json
{ "mail": [] }
```

<h5>With a Announcement</h5>

```json
{
  "mail": [
    {
      "id": "c4effbfe-94ab-4070-9176-cd0860dd1021",
      "sender": { "uid": "1234", "name": "SYBO Games" },
      "header": "Early bird reward!",
      "body": "Thank you for being an early member of the Subway Surfers City crew! To celebrate our first few days, we’re adding this limited edition board to your collection.",
      "expires": "2026-03-31T07:10:00Z",
      "metadata": [],
      "attachments": [
        {
          "type": "boardunlock",
          "id": "board_unlock_classic",
          "value": 1,
          "claimed": null
        }
      ],
      "actions": [],
      "media": [],
      "receiver": { "uid": "0198836e-fb91-7900-9fa4-598349e4a77d" },
      "sent": "2026-02-26T08:48:37.463701Z",
      "read": null
    },
    {
      "id": "d7c6c8f4-a286-4847-b7ec-ce701e98c95e",
      "sender": { "uid": "1234", "name": "SYBO Games" },
      "header": "Thank you for your support!",
      "body": "Thank you for being a part of our soft launch journey! Your feedback and support during our early days has helped us shape this game. Here is an exclusive skin to show our appreciation for your continued support. We wouldn't be here without you!",
      "expires": null,
      "metadata": [],
      "attachments": [
        {
          "type": "skinunlock",
          "id": "skin_unlock_jake_incognito",
          "value": 1,
          "claimed": null
        }
      ],
      "actions": [],
      "media": [],
      "receiver": { "uid": "0198836e-fb91-7900-9fa4-598349e4a77d" },
      "sent": "2026-02-26T08:48:37.47427Z",
      "read": null
    }
  ]
}
```

<h5>With a Announcement (read)</h5>

```json
{
  "mail": [
    {
      "id": "c4effbfe-94ab-4070-9176-cd0860dd1021",
      "sender": { "uid": "1234", "name": "SYBO Games" },
      "header": "Early bird reward!",
      "body": "Thank you for being an early member of the Subway Surfers City crew! To celebrate our first few days, we’re adding this limited edition board to your collection.",
      "expires": "2026-03-31T07:10:00Z",
      "metadata": [],
      "attachments": [
        {
          "type": "boardunlock",
          "id": "board_unlock_classic",
          "value": 1,
          "claimed": null
        }
      ],
      "actions": [],
      "media": [],
      "receiver": { "uid": "0198836e-fb91-7900-9fa4-598349e4a77d" },
      "sent": "2026-02-26T08:48:37.463701Z",
      "read": "2026-02-26T09:52:25.496714Z"
    },
    {
      "id": "d7c6c8f4-a286-4847-b7ec-ce701e98c95e",
      "sender": { "uid": "1234", "name": "SYBO Games" },
      "header": "Thank you for your support!",
      "body": "Thank you for being a part of our soft launch journey! Your feedback and support during our early days has helped us shape this game. Here is an exclusive skin to show our appreciation for your continued support. We wouldn't be here without you!",
      "expires": null,
      "metadata": [],
      "attachments": [
        {
          "type": "skinunlock",
          "id": "skin_unlock_jake_incognito",
          "value": 1,
          "claimed": null
        }
      ],
      "actions": [],
      "media": [],
      "receiver": { "uid": "0198836e-fb91-7900-9fa4-598349e4a77d" },
      "sent": "2026-02-26T08:48:37.47427Z",
      "read": "2026-02-26T09:54:02.597553Z"
    }
  ]
}
```

#### Read

- POST `/v2.0/mail/read`
- Claims the Reward of a Mail
- Sample request (2026-02-26): \
  POST /v2.0/mail/read \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  {
    "id": "f27141a8-b794-4cf8-9555-50bfac5c9b9d"
  }
  ```

<h5>Default Response</h5>

`200 OK`

### Misc

#### Where

- URL `https://where.sybo.net`
- GET `/`
- Get the location data
- Sample request (2026-02-26):
  GET /

- Sample response:

  ```json
  {
    "country": "US",
    "region": "NY",
    "is_us": true,
    "is_eea": false,
    "is_eu": false,
    "is_cmp": false,
    "age_limit": 16,
    "requires_consent": false,
    "requires_age_verification": false
  }
  ```

#### When

- URL `https://when.sybo.net`
- GET `/`
- Get the current time in iso format
- Sample request (2026-02-26):
  GET /

- Sample response:

  ```json
  { "time": "2026-02-26T09:36:07.028Z" }
  ```

### Shop

- POST `/v1.0/shop/purchase`
- ?
- Sample request (2026-06-09): \
  POST /v1.0/shop/purchase \
  Authorization: `Bearer <identityToken>` \
  Body:

  ```json
  {"provider":"google","productId":"surfers.google.prereg.001","receipt":"{\"packageName\":\"com.sybogames.subway.surfers.game\",\"productId\":\"surfers.google.prereg.001\",\"purchaseTime\":1768492955216,\"purchaseState\":0,\"purchaseToken\":\"pfappicnhjnanekpchcbdmgg.AO-J1Ow3Lxe48TP5_Kd14RSuuaHdusSSYbgGaGk...\"}","type":"consumable"}
  ```

<h5>Response</h5>

```json
{"productId":"surfers.google.prereg.001","isTestPurchase":false}
```