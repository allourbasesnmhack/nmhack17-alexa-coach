import boto3
from flask import render_template
from boto3.dynamodb.conditions import Key, Attr

def generateOpportunitiesMessage(userid):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('opportunitydata')

    #search for the user id in the DB passed into function
    response = table.scan(FilterExpression=boto3.dynamodb.conditions.Attr("userid").eq(userid))

    items = response['Items']
    opportunity_list_message = ""
    count=0
#opportunity_list: '{{ subject }} for {{ type }} for {{ regarding }}'
    for item in items:
        count=count+1
        opportunity_list_message += render_template('opportunity_list', subject=item['subject'], type=item['type'], regarding=item['regarding'])
        if count >2:
            break
    return opportunity_list_message
