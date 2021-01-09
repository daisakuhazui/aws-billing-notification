# encoding: utf-8
import unittest
from unittest.mock import patch

from moto import mock_cloudwatch

from src import handler
import pytest
import os
import boto3


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture(scope="function")
def cloudwatch(aws_credentials):
    with mock_cloudwatch():
        yield boto3.client("cloudwatch", region_name="ap-northeast-1")


class HandlerTest(unittest.TestCase):
    """handler.pyのテストクラス"""

    def setUp(self):
        print("Starting Tests...")

    # TODO: warningを修正する
    # TODO: テストが実行できない不具合を修正する
    def test_get_metric_statistics(self):
        statistics = handler.get_metric_statistics()

        self.assertEqual("EstimatedCharges", statistics["Label"])

    def test_build_slack_message_red(self):
        metric_statistics = {"Datapoints": [{"Maximum": 10}]}
        slack_message = handler.build_slack_message(metric_statistics)

        self.assertEqual("AWSどるちぇっかー", slack_message["username"])
        self.assertEqual(":quoca:", slack_message["icon_emoji"])
        self.assertEqual("dummy_channel", slack_message["channel"])
        self.assertEqual("#ff0000", slack_message["attachments"][0]["color"])

    def test_build_slack_message_yellow(self):
        metric_statistics = {"Datapoints": [{"Maximum": 5.0}]}
        slack_message = handler.build_slack_message(metric_statistics)

        self.assertEqual("AWSどるちぇっかー", slack_message["username"])
        self.assertEqual(":quoca:", slack_message["icon_emoji"])
        self.assertEqual("dummy_channel", slack_message["channel"])
        self.assertEqual("warning", slack_message["attachments"][0]["color"])

    def test_build_slack_message_green(self):
        metric_statistics = {"Datapoints": [{"Maximum": 0.0}]}
        slack_message = handler.build_slack_message(metric_statistics)

        self.assertEqual("AWSどるちぇっかー", slack_message["username"])
        self.assertEqual(":quoca:", slack_message["icon_emoji"])
        self.assertEqual("dummy_channel", slack_message["channel"])
        self.assertEqual("good", slack_message["attachments"][0]["color"])

    @patch("requests.post")
    def test_lambda_handler(self, mock_post, cloudwatch):
        event = "dummy_event"
        context = "dummy_context"

        handler.lambda_handler(event, context)
        mock_post.assert_called_once()
