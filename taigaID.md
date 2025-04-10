# Finding Your Taiga User ID

This document explains how to find your Taiga user ID using the Taiga API. This ID is required for the ScrumAgent Discord-Taiga integration.

## Why You Need Your Taiga User ID

The ScrumAgent uses a mapping between Taiga user IDs and Discord usernames in the `taiga_discord_maps.yaml` configuration file. This mapping allows the bot to correctly associate Taiga tasks with Discord users.

## Method: Using the Taiga API Authentication Endpoint

The simplest way to find your Taiga user ID is to make an authentication request to the Taiga API. The response will contain your user information, including your user ID.

### API Endpoint

```
POST /api/v1/auth
```

### Request Body

```json
{
  "type": "normal",
  "username": "your_username",
  "password": "your_password"
}
```

### Example Using ReqBin

1. Go to [ReqBin](https://reqbin.com/curl)
2. Enter the following in the curl command box:

```bash
curl -X POST \
  https://api.taiga.io/api/v1/auth \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "normal",
    "username": "your_username",
    "password": "your_password"
}'
```

3. Replace `https://api.taiga.io` with your Taiga instance URL (from your `.env` file's `TAIGA_API_URL` setting)
4. Replace `your_username` and `your_password` with your actual Taiga credentials
5. Click "Send" to execute the request

### Response

The response will be a JSON object containing your user information. Look for the `id` field, which is your Taiga user ID:

```json
{
  "auth_token": "your-auth-token",
  "refresh": "your-refresh-token",
  "id": 123456,  // This is your Taiga user ID
  "username": "your_username",
  "email": "your.email@example.com",
  "full_name": "Your Full Name",
  "bio": "",
  "photo": null,
  "big_photo": null,
  "gravatar_id": "your-gravatar-id",
  ...
}
```

## Using Your Taiga User ID

Once you have your Taiga user ID, update the `taiga_discord_maps.yaml` file with the correct mapping:

```yaml
taiga_discord_user_map:
  123456: "your_discord_username"  # Replace with your actual Discord username
```

**Important:** Make sure your Discord username in the configuration exactly matches your username in the Discord server, including any special characters or emojis.

## Example for Self-Hosted Taiga

If you're using a self-hosted Taiga instance, adjust the URL accordingly:

```bash
curl -X POST \
  https://your-taiga-instance.com/api/v1/auth \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "normal",
    "username": "your_username",
    "password": "your_password"
}'
```

## Troubleshooting

If you're getting an error about the Discord user not being found, ensure:

1. The Taiga user ID in the configuration is correct
2. The Discord username in the configuration exactly matches your username in the Discord server
3. The ScrumAgent has the necessary permissions to see and interact with your Discord user
