# encoding: utf-8

"""
Testing the poll function of the Bot
"""

from api_secrets import *
import slackclient
import json
import datetime
# import workalendar.europe  # I need MicVisualC++ 14.0... djezus.

cur_date = datetime.datetime.today()

slack_client = slackclient.SlackClient(SLACK_API_KEY)
con_bool = slack_client.rtm_connect(with_team_state=False)

NL_kal_obj = workalendar.europe.Netherlands()
work_day_bool = NL_kal_obj.is_working_day(cur_date)


# Define standard text
message_channel = "own_code"
message_text_tuesday = "Lunch at 12? (Add an emoji) \n Interactive buttons coming soon"
message_text = "Lunch at 12?"

# Define markup text
markup_tuesday = json.dumps([{"text": message_text_tuesday,
                          "fallback": "You are unable to choose an option" ,
                          "callback_id": "lunch_intro",
                          "color" : "#3AA3E3",
                          "attachment_type": "default",
                          "actions": [{"name": "food", "text": ":fish: Kibbeling", "type": "button", "value": "1"},
                                      {"name": "food", "text": ":bread: Regular lunch", "type": "button",
                                       "value": "2"}]}])

# Check if we can post something
send_bool = False
if con_bool:
    print("Bot is connected!")
    if work_day_bool:
        send_bool = True

if send_bool:
    # It is Tuesday!
    if cur_date.isoweekday() == 2:
        slack_client.api_call("chat.postMessage", channel=message_channel, text=" ",
                              attachments=markup_tuesday, as_user=True)
    # Ahw it is not Tuesday
    else:
        slack_client.api_call("chat.postMessage", channel=message_channel, text=message_text)
