# encoding: utf-8

import os

# Slack Notification Setting
# TODO: SSM の SecureString を扱えるようにしたい
SLACK_POST_URL = os.environ["SLACK_AWS_BILLING_NOTIFICATION_WEB_HOOK_URL"]
SLACK_CHANNEL = os.environ["SLACK_AWS_BILLING_NOTIFICATION_CHANNEL_NAME"]
USERNAME = "AWSどるちぇっかー"
ICON = ":quoca:"
