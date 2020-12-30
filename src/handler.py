# encoding: utf-8

import datetime
import json
import logging
import os

import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Slack Notification Setting
# TODO: SSM の SecureString を扱えるようにしたい
# TODO: 設定値を別ファイルに切り出して、テストコードからも参照できるようにしたい
SLACK_POST_URL = os.environ["SLACK_AWS_BILLING_NOTIFICATION_WEB_HOOK_URL"]
SLACK_CHANNEL = os.environ["SLACK_AWS_BILLING_NOTIFICATION_CHANNEL_NAME"]
USERNAME = "AWSどるちぇっかー"
ICON = ":quoca:"


def get_metric_statistics():
    """CloudWatchからメトリクスを取得する"""
    cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")
    metric_statistics = cloudwatch.get_metric_statistics(
        Namespace="AWS/Billing",
        MetricName="EstimatedCharges",
        Dimensions=[{"Name": "Currency", "Value": "USD"}],
        StartTime=datetime.datetime.today() - datetime.timedelta(days=1),
        EndTime=datetime.datetime.today(),
        Period=86400,
        Statistics=["Maximum"],
    )

    print(metric_statistics)

    return metric_statistics


def build_slack_message(metric_statistics):
    """Slackへの通知メッセージを作成する"""
    cost = 0.0
    if metric_statistics["Datapoints"]:
        cost = metric_statistics["Datapoints"][0]["Maximum"]

    date = datetime.datetime.today().strftime("%Y年%m月%d日")

    if float(cost) >= 10.0:
        # red
        color = "#ff0000"
    elif float(cost) > 0.0:
        # yellow
        color = "warning"
    else:
        # green
        color = "good"

    text = "%sまでのAWSの料金は、$%sですゆうたいるい" % (date, cost)

    atachements = {"text": text, "color": color}
    slack_message = {
        "username": USERNAME,
        "icon_emoji": ICON,
        "channel": SLACK_CHANNEL,
        "attachments": [atachements],
    }
    return slack_message


def lambda_handler(event, context):
    """Lambda Handler"""
    # Get metric_statistics from Amazon CloudWatch
    metric_statistics = get_metric_statistics()

    # Build slack massage
    slack_message = build_slack_message(metric_statistics)

    # Post to Slack
    slack_post_url = SLACK_POST_URL
    try:
        req = requests.post(slack_post_url, data=json.dumps(slack_message))
        logger.info("Message posted to %s", slack_message["channel"])
    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", e)
