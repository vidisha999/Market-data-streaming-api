from __future__ import print_function

import base64
import re
import json
print('Loading function')


def lambda_handler(event, context):
    output = []
    succeeded_record_cnt = 0
    failed_record_cnt = 0

    for record in event['records']:
        print(record['recordId'])
        
        print(record['data'])
        
        payload = base64.b64decode(record['data'])
        
        print(payload)

        
        # Lambda function to convert JSON string to CSV format
        to_csv = lambda x: ','.join(map(str, json.loads(x).values()))
        
        # Convert JSON string to CSV
        output_payload = to_csv(payload)
        
        output_payload = output_payload + "\n"
        
        output_payload = output_payload.encode('utf-8')

        output_record = {
                 'recordId': record['recordId'],
                 'result': 'Ok',
                 'data': base64.b64encode(output_payload)
        }
        
        print(output_record)

        output.append(output_record)

    print('Processing completed.  Successful records {}, Failed records {}.'.format(succeeded_record_cnt, failed_record_cnt))
    return {'records': output}