import requests
from utility import get_substring, binary_to_dict
import sys, datetime, hashlib, hmac


def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def get_signature_key(key, date_stamp, region, service):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region)
    k_service = sign(k_region, service)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing


def post(credentials, endpoint, stage, payload):
    service = 'execute-api'
    method = 'POST'
    host = get_substring(endpoint, start = "'https://", stop = '/' + stage + '/')
    uri = get_substring(endpoint, start = host, stop = '')
    content_type = 'application/json'
    dict_credentials = credentials
    region = dict_credentials['region']

    if(dict_credentials['account'] == "iot-mvp-devqual"):
        securitytoken = ''
    else:
        securitytoken = dict_credentials['aws_security_token']

    secretkey = dict_credentials['aws_secret_access_key']
    accesskey = dict_credentials['aws_access_key_id']

    if accesskey is None or secretkey is None:
        print('No access key is available.')
        sys.exit()
    
    t = datetime.datetime.utcnow()
    amz_date = t.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = t.strftime('%Y%m%d')

    canonical_uri = uri
    canonical_querystring = ''
    canonical_headers = 'content-type:' + content_type + '\n' + 'host:' + host + '\n' + 'x-amz-date:' + amz_date + '\n'
    signed_headers = 'content-type;host;x-amz-date'
    payload_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()

    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = date_stamp + '/' + region + '/' + service + '/' + 'aws4_request'

    string_to_sign = algorithm + '\n' +  amz_date + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

    signing_key = get_signature_key(secretkey, date_stamp, region, service)

    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    authorization_header = algorithm + ' ' + 'Credential=' + accesskey + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    if(dict_credentials["account"] == "iot-mvp-devqual"):

        headers = {'Content-Type':content_type,
            'x-amz-date':amz_date,
            'Authorization':authorization_header}

    else:
        headers = {'Content-Type':content_type,
            'x-amz-date':amz_date,
            'x-amz-security-token': securitytoken,
            'Authorization':authorization_header}
    
    r = requests.post(endpoint, data=payload, headers=headers)
    post_response = (r.status_code, r._content)

    return post_response


def get(credentials_g, endpoint, commandId, environmentPrefix, env):
    service = 'execute-api'
    method = 'GET'
    endpoint_g = endpoint + commandId
    host = get_substring(endpoint, start = "'https://", stop = '/'+ env)
    uri = get_substring(endpoint, start = host, stop = "") + commandId
    content_type = 'application/json'
    request_parameters = 'index=jobs_' + environmentPrefix + '_%2A'

    dict_cred_g = credentials_g
    region = dict_cred_g['region']
    securitytoken = dict_cred_g['aws_security_token']

    secretkey = dict_cred_g['aws_secret_access_key']
    accesskey = dict_cred_g['aws_access_key_id']

    if accesskey is None or secretkey is None:
        print('No access key is available.')
        sys.exit()

    t = datetime.datetime.utcnow()
    amzdate = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d')

    canonical_uri = uri
    canonical_querystring = request_parameters
    canonical_headers = 'content-type:' + content_type + '\n' + 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'
    signed_headers = 'content-type;host;x-amz-date'
    payload_hash = hashlib.sha256(('').encode('utf-8')).hexdigest()

    canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'

    string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

    signing_key = get_signature_key(secretkey, datestamp, region, service)

    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    authorization_header = algorithm + ' ' + 'Credential=' + accesskey + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

    headers = {'Content-Type': content_type,
        'host':host,
        'x-amz-security-token':securitytoken, 
        'x-amz-date':amzdate,
        'Authorization':authorization_header
        }

    request_url = endpoint_g + '?' + canonical_querystring

    response_g = requests.get(request_url, headers=headers)

    if(response_g.status_code == 404):
        return get(credentials_g, endpoint, commandId, environmentPrefix, env)
    elif(response_g.status_code == 403):
        message = binary_to_dict(response_g._content)["message"]
        response = (response_g.status_code, message)
        return response
    elif(response_g.status_code == 400):
        message = str(response_g._content)
        response = (response_g.status_code, message)
        return response
    elif(response_g.status_code == 200 and binary_to_dict(response_g._content)["hits"]["max_score"] != None):
        if(binary_to_dict(response_g._content)["hits"]["documents"] != [] and binary_to_dict(response_g._content)["hits"]["documents"][0]["status"] == "SUCCEEDED" ):
            message = binary_to_dict(response_g._content)["hits"]["documents"][0]["statusDetails"]["thing_id"]
        else:
            message = binary_to_dict(response_g._content)["hits"]["documents"][0]["status"]
        response = (response_g.status_code, message)
        return response
    else:
        message = "JOB DOESN'T CREATED, YET"
        response = (response_g.status_code,message)
        return response