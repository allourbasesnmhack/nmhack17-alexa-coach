import boto3
import random
from flask import render_template
from boto3.dynamodb.conditions import Key, Attr

my_pick = ""

def generateTipsMessage( userid ):
    # tips_message = "Here's a tip Derek... Just the tip!"
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('tips')

    response = table.scan (
        FilterExpression=Attr("goal_name").eq('factfinder')
    )

    items = response['Items']
    index_count = len(items)
    my_pick = random.randrange(index_count)

    return items[my_pick]['message']



    # print response
    # items = response['Items']
    # tips_message = ""
    # for item in items:
    #     print item['tips_message']

    # return response[0]
