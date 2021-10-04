def json_response(**kwargs):
    data = '{ '
    for k, v in kwargs.items():
        data += '"%s":"%s", ' % (k, v)

    data = data[:-2] + '}'
    return data
