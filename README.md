# cyberattack-forecasting
This repository holds the algorithm to forecast cyberattacks by using social media posts.

## Getting started
To be able to run the project please proceed with following steps:
1. Create a `.env` file with the follwing content:
```bash
MONGO_INITDB_ROOT_USERNAME={{USERNAME}}
MONGO_INITDB_ROOT_PASSWORD={{PASSWORD}}
MONGO_INITDB_DATABASE=cyberthreat
MONGO_DUMP_FILE=./docker-entrypoint-initdb.d/mongo/
MONGO_DATA_VOLUME_NAME={{VOLUME_NAME}}
```
2. Run the following command to build and initialize a docker container with a preloaded instance of 
a Mongo database:
```bash
docker-compose up -d --build
```

3. Generate credentials for MongoDB and Twitter clients:
    - With a yaml file containing the following structure:
```yaml
[TWITTER_CREDENTIALS_KEYS]:
  consumer_key: <API_KEY>
  consumer_secret: <API_KEY_SECRET>
  bearer_token: <BEARER_TOKEN>
  access_token: <ACCESS_TOKEN>
  access_token_secret: <ACCESS_TOKEN_SECRET>

[MONGO_CREDENTIALS_KEY]:
  user: <MONGO_USERNAME>
  password: <MONGO_PASSWORD>
  host: <MONGO_HOST>
  port: <MONGO_PORT>
```
    
- With environment variables:
```bash
# Twitter credentials
TWITTER_API_KEY=<API_KEY>
TWITTER_API_SECRET_KEY=<API_KEY_SECRET>
TWITTER_BEARER_TOKEN=<BEARER_TOKEN>
TWITTER_ACCESS_TOKEN=<ACCESS_TOKEN>
TWITTER_ACCESS_TOKEN_SECRET=<ACCESS_TOKEN_SECRET>

# Mongo credentials
MONGO_USER=<MONGO_USERNAME>
MONGO_PASSWORD=<MONGO_PASSWORD>
MONGO_HOST=<MONGO_HOST>
MONGO_PORT=<MONGO_PORT>
```