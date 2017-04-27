import boto3
from flask import render_template
from boto3.dynamodb.conditions import Key, Attr

def generateActivitiesMessage(userid):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('activitydata')
    response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr("userid").eq(userid))

    items = response['Items']
    activity_list_message = ""
    for item in items:
        activity_list_message += render_template('activity_list', regarding=item['regarding'], segment=item['segment'], type=item['type'], subject=item['subject'])
    return activity_list_message
