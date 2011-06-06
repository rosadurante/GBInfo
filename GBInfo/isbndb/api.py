

import httplib2
import json

from urllib import urlencode
from xml.dom.minidom import parse, parseString


"""
Request to isbndb.com
----------------------

+-------------------------------------------------------------------+
| All:          ?access_key=...&results=details&page_number=...     |
+-------------------------------------------------------------------+
| Title:        http://isbndb.com/api/books.xml                     |
|               &index1=title&value1=...                            |
+--------------------------------------------------------------------
| ISBN:         http://isbndb.com/api/books.xml                     |
|               &index1=isbn&value1=...                             |
+-------------------------------------------------------------------+
| Author:       http://isbndb.com/api/authors.xml                   |
|               &index1=name&value1=... # GET person_id:            |
|                 # <AuthorData person_id=..>                       |
|               http://isbndb.com/api/book.xml                      |
|               &index1=person_id&value1=<getted value/s>           |
+-------------------------------------------------------------------+
| Publisher:    http://isbndb.com/api/publishers.xml                |
|               &index1=name&value1=... # GET publisher_id:         |
|                 # <PublisherData publisher_id=...>                |
|               http://isbndb.com/api/books.xml                     |
|               &index1=publisher_id&value1=<getted value/s>        |
+-------------------------------------------------------------------+
| Subject:      http://isbndb.com/api/subjects.xml                  |
|               &index1=name&value1=... # GET subject_id:           |
|                 # <SubjectData subject_id=...>                    |
|               http://isbndb.com/api/books.xml                     |
|               &index1=subject_id&value1=<getted value/s>          |
+-------------------------------------------------------------------+

Examle
------

<ISBNdb>
  <BookList total_results=''>
    <BookData book_id='' isbn=''>
      <Title></Title>
      <TitleLong></TitleLong>
      <AuthorsText></AuthorsText>
      <PublisherText></PublisherText>
      <Details change_time='' edition_info='' language='' physical_description_text='' />
    </BookData>
    <BookData>
      ...
    </BookData>
  </BookList>
</ISBNdb>
"""


def request(url, datas):
    h = httplib2.Http()

    # Get key from settings
    get_key(datas)

    # Make request and get datas
    urlrequest = url + urlencode(datas)
    resp, content = h.request(urlrequest, 'GET')

    # Error handler
    if resp['status'] != '200':
        return {'HttpError': resp['status']}
    elif '<ErrorMessage>' in content:
        return {'KeyError': None}

    return parse_response(url, content)


def get_key(datas):
    import settings
    f = open(settings.CONFIG_FILE, 'r')

    key = f.read()
    if '\n' in key:
        key = json.loads(key[:-1])
    else:
        key = json.loads(key)

    datas['access_key'] = key['keygen']


def parse_response(url, content):
    xml = parseString(content)
    datas = None
    if 'authors' in url:
        datas = {'Element': 'AuthorData',
                 'Attribute': 'person_id'}
    elif 'publishers' in url:
        datas = {'Element': 'PublisherData',
                 'Attribute': 'publisher_id'}
    elif 'subjects' in url:
        datas = {'Element': 'SubjectData',
                 'Attribute': 'subject_id'}

    return parse_datas(xml, datas)


def parse_datas(content, datas=None):
    if datas:
        elements = content.getElementByTagName(datas['Element'])
        attr_id = []
        for elem in elements:
            attributes = elem.attributes.items()
            for attr in attributes:
                if attr[0] is datas['Attribute']:
                    attr_id.append(attr[1])

        return {datas['Attribute']: attr_id}
    else:
        xml = []
        bookdata = content.getElementByTagName('BookData')
        for item in bookdata:
            book = {}
            attributes = item.attributes.items()
            for attr in attributes:
                book[attr[0]] = attr[1]
        title = content.getElementByTagName('Title')
