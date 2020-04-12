"""
Helpers for sending requests with a test client.
"""
import json


def send_get(client, route, headers=None, data=None, key=None, 
        follow_redirects=False):
    """Helper method for sending GET requests to the test client.
    :param client: the test client
    :param route: the route to send the request to
    :param headers: headers to send with the request
    :param data: data to send
    :param key: key for authorization
    :param follow_redirects: whether to follow redirects or not
    :return: the request response
    """
    return send_request(client, route, headers=headers, data=data, key=key,
        follow_redirects=follow_redirects)


def send_post(client, route, headers=None, data=None, key=None, 
        follow_redirects=True):
    """Helper method for sending GET requests to the test client.
    :param client: the test client
    :param route: the route to send the request to
    :param headers: headers to send with the request
    :param data: data to send
    :param key: key for authorization
    :param follow_redirects: whether to follow redirects or not
    :return: the request response
    """
    return send_request(client, route, headers=headers, data=data, key=key,
        method='POST', content_type='application/x-www-form-urlencoded',
        follow_redirects=follow_redirects)


def send_request(client, route, headers=None, data=None,
        content_type='text/html', key=None, method='GET',
        follow_redirects=False):
    """Helper method for sending requests to the test client.
    :param client: the test client
    :param route: the route to send the request to
    :param headers: headers to send with the request
    :param data: data to send
    :param content_type: request content type
    :param key: key for authorization
    :param method: the method to send the request with
    :param follow_redirects: whether to follow redirects or not
    :return: the request response
    """
    methods = {
        'GET': client.get,
        'POST': client.post,
        'PUT': client.put,
        'DELETE': client.delete,
    }
    if method in methods:
        if key:
            if headers:
                data.update({'Authorization': f'Bearer {key}'})
            else:
                headers = {'Authorization': f'Bearer {key}'}
    
        return methods[method](
            route,
            headers=headers,
            data=data,
            content_type=content_type,
            follow_redirects=follow_redirects
        )