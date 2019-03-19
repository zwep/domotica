# encoding: utf-8

"""
Amazing SlackBot messages... every day at 11:45 it will execute this file by using cron.
"""

from api_secrets import *
import slackclient
import datetime
import workalendar.europe

cur_date = datetime.datetime.today()

slack_client = slackclient.SlackClient(SLACK_API_KEY)
con_bool = slack_client.rtm_connect(with_team_state=False)

NL_kal_obj = workalendar.europe.Netherlands()
work_day_bool = NL_kal_obj.is_working_day(cur_date)

# This gives an overview of ALL the possible channels.
# Slack Bot can only participate in channels where it is invite to
# res_channel = slack_client.api_call("channels.list")

# message_channel = "lunch"
message_channel = "own_code"
message_text = "Lunch at 12?"
# message_text = "This is a test message"

if con_bool:
    print("Bot is connected!")
    if work_day_bool:
        slack_client.api_call("chat.postMessage", channel=message_channel, text=message_text)
    else:
        print("Today, we don't work")
else:
    print("Bot is not connected.")
