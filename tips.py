import boto3
from flask import render_template
from boto3.dynamodb.conditions import Key, Attr

def generateTipsMessage( goal_name ):
    tips_message = "Here's a tip"
    # dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # table = dynamodb.Table('tips')
    # response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr("userid").eq(userid))
    #
    # items = response['Items']
    # tips_message = ""
    # for item in items:
    #     print item['tips_message']
    return tips_message
