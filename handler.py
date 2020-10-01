# encoding: utf-8

import json
import datetime
import requests
import boto3
import os
import logging
from base64 import b64decode

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Slack Notification Setting
# TODO SSM の SecureString を扱えるようにしたい
SLACK_POST_URL = os.environ[
    'SLACK_AWS_BILLING_NOTIFICATION_WEB_HOOK_URL']
SLACK_CHANNEL = os.environ['SLACK_AWS_BILLING_NOTIFICATION_CHANNEL_NAME']

response = boto3.client('cloudwatch', region_name='us-east-1')


def get_metric_statistics():
    metric_statistics = response.get_metric_statistics(
        Namespace='AWS/Billing',
        MetricName='EstimatedCharges',
        Dimensions=[
            {
                'Name': 'Currency',
                'Value': 'USD'
            }
        ],
        StartTime=datetime.datetime.today() - datetime.timedelta(days=1),
        EndTime=datetime.datetime.today(),
        Period=86400,
        Statistics=['Maximum'])
    return metric_statistics


def build_slack_message():
    metric_statistics = get_metric_statistics()
    cost = metric_statistics['Datapoints'][0]['Maximum']
    date = metric_statistics['Datapoints'][0]['Timestamp'].strftime(
        '%Y年%m月%d日')
    if float(cost) >= 10.0:
        # red
        color = "#ff0000"
    elif float(cost) > 0.0:
        # yellow
        color = "warning"
    else:
        # green
        color = "good"

    text = "%sまでのAWSの料金は、$%sです。" % (date, cost)

    atachements = {"text": text, "color": color}
    slack_message = {
        'channel': SLACK_CHANNEL,
        "attachments": [atachements],
    }
    return slack_message


def lambda_handler(event, context):
    slack_message = build_slack_message()
    # Post to Slack
    try:
        req = requests.post(SLACK_POST_URL, data=json.dumps(slack_message))
        logger.info("Message posted to %s", slack_message['channel'])
    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", e)
