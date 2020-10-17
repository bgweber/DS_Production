def lambda_handler(event, context):
    
    return {
        'statusCode': 200,
        'body': event['msg']
    }