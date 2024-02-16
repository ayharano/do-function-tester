from datetime import datetime, timezone
from http import HTTPStatus


def main(args):
    received_at = datetime.now(timezone.utc).isoformat()

    sent_at_arg = args.get("sent_at")
    list_args = args.get("list_args", [])

    return {
        "statusCode": HTTPStatus.ACCEPTED,
        "body": {
            "sent_at_arg": sent_at_arg,
            "list_args": list_args,
            "received_at": received_at,
        },
    }
