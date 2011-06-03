

import httplib2

from urllib import urlencode


def request(datas):
    h = httplib2.HTTP()

    get_key(datas)

    url = 'http://isbndb.com/api/books.xml?' + urlencode(datas)
    resp, content = h.request(url, 'GET')

    if resp['status'] != 200:
        print "Error " + resp['status']
        return {}
    elif '<ErrorMessage>' in content:
        print "Error with Access_Key"
        return {}
    else:
        return parse_response(content)


def get_key(datas):
    # Obtener basedir (settings o algo)
    # f = open(.config, r)
    # a = f.read()
    # json.loads(a[:-1])
    pass


def parse_response(content):
    pass
