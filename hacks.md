# Explanations

## Table of Contents

- [Explanations](#explanations)
  - [Table of Contents](#table-of-contents)
  - [Spoof Requests](#spoof-requests)
    - [Get Mails with Rewards](#get-mails-with-rewards)
    - [Play with Experiments](#play-with-experiments)

## Spoof Requests

You will need a PC and your phone for this.

You can use a programm called [reqable](https://reqable.com) \
You'll need to have rooted your phone or ssl-bypassed the app or you can use [revanced.app](https://revanced.app) (in the setting enable "Show universal patches"). \
Select the patch "Override certificate pinning".

Install the required certificates from the client onto your Phone as a "CA Certificate". \
Connect the phone to the PC client.

After patching the app and installing it open the programm. \
Copy this code into a file called `reqable-rewrites.config` \
In "Tools" go to "Rewrite" click on the "Import" button and import the config.

Open then app, it will then redirect the requests.

> [!IMPORTANT]
> Remember this bypassing only works while the client and app on both PC and phone are running and are connected.

### Get Mails with Rewards

<details>
  <summary>reqable-rewrites.config</summary>

```json
[
  {
    "id": "1a7ddc8e-0884-4112-a3e6-e1716852b77e",
    "name": "Get Mail",
    "method": "",
    "url": "https://subwaycity.prod.sybo.net/v2.0/mail",
    "wildcard": false,
    "action": {
      "type": 2,
      "headers": [{ "key": "Date", "value": "Fri, 13 Feb 2026 17:05:59 GMT" }],
      "body": {
        "type": 1,
        "payload": "{\n  \"mail\": [\n    {\n      \"id\": \"84677b77-78ab-402c-87ee-3cbb21ac60d1\",\n      \"sent\": \"2026-02-13T12:00:00Z\",\n      \"read\": null,\n      \"expires\": null,\n      \"sender\": {\n        \"uid\": \"1234\",\n        \"name\": \"SYBO Games\"\n      },\n      \"receiver\": {\n        \"uid\": \"84ecaff3-d517-4efe-a9b1-47fb8fd702f7\"\n      },\n      \"header\": \"Double Coins Test 3 - Luke X 2 attachments\",\n      \"body\": \"Double Coins Test 3 - Luke X 2 attachments\",\n      \"metadata\": null,\n      \"attachments\": [\n        {\n          \"type\": \"Currency\",\n          \"id\": \"Coins\",\n          \"value\": 42\n        }\n      ]\n    }\n  ]\n}"
      },
      "statusLineEnabled": true,
      "headersEnabled": false,
      "bodyEnabled": true
    },
    "isEnabled": true
  }
]
```

</details>

You can also change the Mail code

<details>
  <summary>Mail Body</summary>

```json
{
  "mail": [
    {
      "id": "84677b77-78ab-402c-87ee-3cbb21ac60d1",
      "sent": "2026-02-13T12:00:00Z",
      "read": null,
      "expires": null,
      "sender": {
        "uid": "1234",
        "name": "SYBO Games"
      },
      "receiver": {
        "uid": "84ecaff3-d517-4efe-a9b1-47fb8fd702f7"
      },
      "header": "Double Coins Test 3 - Luke X 2 attachments",
      "body": "Double Coins Test 3 - Luke X 2 attachments",
      "metadata": null,
      "attachments": [
        {
          "type": "Currency",
          "id": "Coins",
          "value": 42
        },
        {
          "type": "Currency",
          "id": "Coins",
          "value": 42
        }
      ]
    }
  ]
}
```

</details>

<details>
  <summary>attachments</summary>

```json
{
  "type": "Currency",
  "id": "Coins",
  "value": 42
}
```

```json
{
  "type": "Currency",
  "id": "Hoverboards",
  "value": 3
}
```

```json
{
  "type": "Currency",
  "id": "Keys",
  "value": 3
}
```

```json
{
  "type": "Currency",
  "id": "EventCoins",
  "value": 50
}
```

```json
{
  "type": "Hoverboard",
  "id": "confetticrush",
  "value": 1
}
```

```json
{
  "type": "Character",
  "id": "rebecaroar.purrfectionOutfit",
  "value": 1
}
```

</details>

### Play with Experiments

You can replace the variantId with the needed experiment.

<details>
  <summary>reqable-rewrites.config</summary>

```json
[
  {
    "id": "e41494ff-99f0-4bfe-abc1-287aaba9f959",
    "name": "MatchExperiments",
    "method": "",
    "url": "https://subwaycity.prod.sybo.net/rpc/abtesting.ext.v2.PrivateService/MatchExperiments",
    "wildcard": false,
    "action": {
      "type": 2,
      "code": 200,
      "headers": [{ "key": "Content-Type", "value": "application/json" }],
      "body": {
        "type": 1,
        "payload": "{\n  \"experiments\": [\n    {\n      \"experimentId\": \"ab_reduced_max_tickets_2.1.0\",\n      \"variantId\": \"ab_ticketing_variant_b\",\n      \"variantType\": \"VARIANT_TYPE_GAMEDATA\",\n      \"endAt\": \"2126-04-01T08:04:15.544Z\"\n    }\n  ]\n}"
      },
      "statusLineEnabled": true,
      "headersEnabled": true,
      "bodyEnabled": true
    },
    "isEnabled": true
  }
]

```

</details>
