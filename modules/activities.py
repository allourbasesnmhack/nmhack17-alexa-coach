import boto3
from flask import render_template
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
def generateActivitiesMessage(userid):

    table = dynamodb.Table('activitydata')
    response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr("userid").eq(userid))

    items = response['Items']
    activity_list_message = ""
    count=0
    for item in items:
        count=count+1
        activity_list_message += render_template('activity_list', regarding=item['regarding'], segment=item['segment'], type=item['type'], subject=item['subject'])
        if count >2:
            break
    return activity_list_message

def countactivities(userid):
    activities_table = dynamodb.Table('goals')
    response = activities_table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('userid').eq(userid))
    activities_items = response['Items']
    # print activities_items
    count = 0
    for activity_item in activities_items:
        count = count + int(activity_item['actual'])
    return count
