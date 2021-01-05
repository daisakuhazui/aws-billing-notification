# encoding: utf-8

import datetime
import json
import logging

import boto3
import requests

from config import variables


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_metric_statistics():
    """
    CloudWatchからメトリクスを取得

    検索期間は月始めの1日9:00から、Lambda関数実行時の9:00まで
    """
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
    """
    Slackへの通知メッセージを作成

    メッセージの色分け条件
        10.0$以上: 赤
        5.0$以上: 黄
        0.0$以上: 緑
    """
    cost = 0.0
    if metric_statistics["Datapoints"]:
        cost = metric_statistics["Datapoints"][0]["Maximum"]

    date = datetime.datetime.today().strftime("%Y年%m月%d日")

    if float(cost) >= 10.0:
        # red
        color = "#ff0000"
    elif float(cost) > 5.0:
        # yellow
        color = "warning"
    else:
        # green
        color = "good"

    text = "%sまでのAWSの料金は、$%sですゆうたいるい" % (date, cost)

    atachements = {"text": text, "color": color}
    slack_message = {
        "username": variables.USERNAME,
        "icon_emoji": variables.ICON,
        "channel": variables.SLACK_CHANNEL,
        "attachments": [atachements],
    }
    return slack_message


def lambda_handler(event, context):
    """
    Lambda Handler

    handler.py内で定義された関数を呼び出し、AWS利用料金をSlack通知する。
    """
    # Get metric_statistics from Amazon CloudWatch
    metric_statistics = get_metric_statistics()

    # Build slack massage
    slack_message = build_slack_message(metric_statistics)

    # Post to Slack
    slack_post_url = variables.SLACK_POST_URL
    try:
        requests.post(slack_post_url, data=json.dumps(slack_message))
        logger.info("Message posted to %s", slack_message["channel"])
    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", e)
