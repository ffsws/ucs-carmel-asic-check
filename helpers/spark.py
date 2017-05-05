import requests

def send_spark_message(token, roomId, md):
    """
    sends a markdown message to a spark room
    :param token: str your token
    :param roomId: str room id
    :param msg: str message text
    :return:
    """
    url = 'https://api.ciscospark.com/v1/messages'
    headers = {"authorization": "Bearer {}".format(token)}
    payload = {"roomId": roomId,
               "markdown": md}
    resp = requests.post(url, headers=headers, data=payload)
    return resp
