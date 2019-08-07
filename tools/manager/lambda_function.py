import json
from database import Database


def lambda_handler(event, context):
    # TODO implement

    print("Connecting")
    db = Database("")
    print("test db")
    pass

    db.delete_player("test3")
    db.add_player("test3", "/path3")

    test = db.get_player(("test3",))

    print(test)

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
