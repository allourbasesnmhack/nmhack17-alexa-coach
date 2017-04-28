import boto3
from flask import render_template
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
def generateActivitiesMessage(userid):

    table = dynamodb.Table('activitydata')
    response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr("userid").eq(userid))

    items = response['Items']
    activity_list_message = ""
    for item in items:
        activity_list_message += render_template('activity_list', regarding=item['regarding'], segment=item['segment'], type=item['type'], subject=item['subject'])
    return activity_list_message

def countActivites(userid):
    activities_table = dynamodb.Table('activities')
    response = activities_table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('userid').eq(userid))
    activities_items = response['Items']
    # print activities_items
    count = 0
    for activity_item in activities_items:
        count = count + int(activity_item['count'])
    return count