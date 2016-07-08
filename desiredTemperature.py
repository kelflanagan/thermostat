from __future__ import print_function

import json
import boto3
import httplib

""" client ID is a value obtained from google when a client device is 
    registered with google. In this case I am treating this lambda function
    like a device that has a screen where users can be told what to do, but
    have to go to a computer to authorize it. The clientID is stored in the
    dynamoDB store under the Global seciton"""
def getClientID():
    # connect to db
    db = boto3.client('dynamodb')
    # find the item labelled 'Global'
    response = db.get_item(
        TableName='desiredTemperature',
        Key={
            'level+room' : {'S' : 'Global'}
        }
    )
    return response['Item']['clientID']['S']


""" Use the clientID to post a request to google to obtain the user_code
    and the verification_code from google. These will then be presented to
    the user who will enter them into a web browser. Since the lambda function
    does not have a screen, I am hoping to text message it or email it to the
    user."""
def getGoogleUserCodeAndVerificationURL():
    # get client ID for google call
    clientID = getClientID()
    
    # form call components and make google call
    body = 'client_id=' + clientID + '&scope=email profile https://www.googleapis.com/auth/calendar.readonly'
    google = httplib.HTTPSConnection('accounts.google.com')
    google.request('POST', '/o/oauth2/device/code', body, {"Content-Type": "application/x-www-form-urlencoded"})
    
    #get and form result
    result = json.loads(google.getresponse().read())
    return result['verification_url'], result['user_code']


def getDesiredTemperature(event, context):
    # authorize use of google calendar
    # perform dynamoDB lookup for client ID
    verificationURL, userCode = getGoogleUserCodeAndVerificationURL()

    #if 'Item' not in response:
    #    return "Device not found"
    #else:
    #    queryLocation = response['Item']['queryLocation']['S']
    #    previousDesiredTemperature = response['Item']['desiredTemperature']['N']
    # concatenate level and room to create lookup key
    #lookupKey = event['level'] + event['room']
    
    # perform dynamoDB lookup for previous desired temperature and URL
    # if DB query doesn't work 'Item' will not be found in dictionary
    
    #response = db.get_item(
    #    TableName='desiredTemperature',
    #    Key={
    #        'level+room' : {'S' : lookupKey}
    #    }
    #)
    #if 'Item' not in response:
    #    return "Device not found"
    #else:
    #    queryLocation = response['Item']['queryLocation']['S']
    #    previousDesiredTemperature = response['Item']['desiredTemperature']['N']
    #print(response)
    #item = response['Item']
    #print("GetItem succeeded:")
    #print(json.dumps(item, indent=4, cls=DecimalEncoder))
    
    #print("context == " + context.invoked_function_arn)
    #print("Received event: " + json.dumps(event, indent=2))

    return userCode
