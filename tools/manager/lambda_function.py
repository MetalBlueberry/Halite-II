import json
from database import Database


def generate_player_from_key(key:str):
    file = key.split('/')[-1]
    file_name = file.split('.')[0]

    path = "docker run --rm -i %s:latest" % file_name
    return file_name, path

def RegisterBotOnS3Upload(event, context):
    key = event['Records'][0]['s3']['object']['key']
    print(key)
    name, path = generate_player_from_key(key)
    print(name, path)

    print("Connecting")
    db = Database("haliteTest")
    print("test db")
    pass

    db.delete_player(name)
    db.add_player(name, path)

    return {
        'statusCode': 200,
        'body': event
    }

def test_RegisterBotOnS3Upload():
    input_event_string = "{\"Records\": [{\"eventVersion\": \"2.0\", \"eventSource\": \"aws:s3\", \"awsRegion\": \"us-east-1\", \"eventTime\": \"1970-01-01T00:00:00.000Z\", \"eventName\": \"ObjectCreated:Put\", \"userIdentity\": {\"principalId\": \"EXAMPLE\"}, \"requestParameters\": {\"sourceIPAddress\": \"127.0.0.1\"}, \"responseElements\": {\"x-amz-request-id\": \"EXAMPLE123456789\", \"x-amz-id-2\": \"EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH\"}, \"s3\": {\"s3SchemaVersion\": \"1.0\", \"configurationId\": \"testConfigRule\", \"bucket\": {\"name\": \"example-bucket\", \"ownerIdentity\": {\"principalId\": \"EXAMPLE\"}, \"arn\": \"arn:aws:s3:::example-bucket\"}, \"object\": {\"key\": \"bots/hbot.tar\", \"size\": 1024, \"eTag\": \"0123456789abcdef0123456789abcdef\", \"sequencer\": \"0A1B2C3D4E5F678901\"}}}]}"
    input_event = json.loads(input_event_string)
    response = RegisterBotOnS3Upload(input_event, None)
    print(response)


if __name__ == "__main__":
    test_RegisterBotOnS3Upload()