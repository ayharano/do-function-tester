import argparse
import os
from datetime import datetime, timezone
from pprint import pprint

import requests
from dotenv import load_dotenv


def prepare_argparser():
    parser = argparse.ArgumentParser(
        prog="tester",
        description="Test Call a Function Asynchronously and Retrieve Activation Records",
        epilog="Required env vars: FUNCTION_URL, AUTHORIZATION_TOKEN",
    )

    subparsers = parser.add_subparsers(help="commands", required=True, dest="command")

    # issue command
    issue_parser = subparsers.add_parser(
        "issue",
        description="Issue Asynchronous Function Call",
        help="Issue Asynchronous Function Call",
    )
    issue_parser.add_argument(
        "list_args",
        action="store",
        nargs="*",
        help="optional values to be sent to the Function as a list",
    )

    # retrieve subparser
    parser_retrieve = subparsers.add_parser(
        "retrieve",
        description="Retrieve Activation Record",
        help="Retrieve Activation Record",
    )
    parser_retrieve.add_argument(
        "activationId",
        action="store",
        help="activationId to be retrieved",
    )

    return parser


def issue(*, function_url, authorization_token, list_args):
    sent_at = datetime.now(timezone.utc).isoformat()
    headers = {
        # Details at https://docs.digitalocean.com/products/functions/how-to/async-functions/#call-a-function-asynchronously-using-curl-and-the-rest-api
        "Authorization": authorization_token,
    }
    params = {"blocking": "false"}
    payload = {
        "sent_at": sent_at,
        "list_args": list_args,
    }
    timeout_in_seconds = 5.0

    before_request = datetime.now(timezone.utc)
    response = requests.post(
        function_url,
        headers=headers,
        params=params,
        json=payload,
        timeout=timeout_in_seconds,
    )
    after_request = datetime.now(timezone.utc)

    pprint(
        {
            "status_code": response.status_code,
            "body": response.json(),
            "before_request": before_request.isoformat(),
            "after_request": after_request.isoformat(),
            "time_diff": (after_request - before_request).total_seconds(),
        }
    )


def retrieve(*, function_url, authorization_token, activationId):
    namespace_url = function_url[: function_url.find("/actions")]
    activation_url = f"{namespace_url}/activations/{activationId}"
    headers = {
        # Details at https://docs.digitalocean.com/products/functions/how-to/async-functions/#call-a-function-asynchronously-using-curl-and-the-rest-api
        "Authorization": authorization_token,
    }
    timeout_in_seconds = 5.0

    before_request = datetime.now(timezone.utc)
    response = requests.get(
        activation_url,
        headers=headers,
        timeout=timeout_in_seconds,
    )
    after_request = datetime.now(timezone.utc)

    pprint(
        {
            "status_code": response.status_code,
            "body": response.json(),
            "before_request": before_request.isoformat(),
            "after_request": after_request.isoformat(),
            "time_diff": (after_request - before_request).total_seconds(),
        }
    )


if __name__ == "__main__":
    load_dotenv()

    parser = prepare_argparser()

    args_ = parser.parse_args()

    function_url_ = os.environ.get("FUNCTION_URL", "")
    authorization_token_ = os.environ.get("AUTHORIZATION_TOKEN", "")

    for value, name in (
        (function_url_, "FUNCTION_URL"),
        (authorization_token_, "AUTHORIZATION_TOKEN"),
    ):
        if not value:
            raise ValueError(f"Missing environment variables {name}")

    match args_:
        case argparse.Namespace(command="issue"):
            issue(
                function_url=function_url_,
                authorization_token=authorization_token_,
                list_args=args_.list_args,
            )
        case argparse.Namespace(command="retrieve"):
            retrieve(
                function_url=function_url_,
                authorization_token=authorization_token_,
                activationId=args_.activationId,
            )
