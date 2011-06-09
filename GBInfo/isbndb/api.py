

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
    datas['access_key'] = settings.ISBNDB_KEY


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
        elements = content.getElementsByTagName(datas['Element'])
        attr_id = []
        for elem in elements:
            attributes = elem.attributes.items()
            for attr in attributes:
                if attr[0] is datas['Attribute']:
                    attr_id.append(attr[1])

        return {datas['Attribute']: attr_id}
    else:
        xml = {}
        # Just one 'BookList' in all response
        booklist = content.getElementsByTagName('BookList')[0]
        xml['results'] = booklist.getAttribute('total_results')

        xml['books'] = []
        bookdata = content.getElementsByTagName('BookData')
        for item in bookdata:
            book = {}
            book['book_id'] = item.getAttribute('book_id')
            book['isbn'] = item.getAttribute('isbn')

            title = item.getElementsByTagName('Title')[0]  # Just only one title
            try:
                book['title'] = title.firstChild.nodeValue
            except AttributeError:
                book['title'] = None

            titlelong = item.getElementsByTagName('TitleLong')[0]
            try:
                book['titlelong'] = titlelong.firstChild.nodeValue
            except AttributeError:
                book['titlelong'] = None

            authors = item.getElementsByTagName('AuthorsText')[0]
            try:
                book['authors'] = authors.firstChild.nodeValue
            except AttributeError:
                book['authors'] = None

            publishers = item.getElementsByTagName('PublisherText')[0]
            try:
                book['publishers'] = authors.firstChild.nodeValue
            except AttributeError:
                book['publishers'] = None

            details = item.getElementsByTagName('Details')[0]
            book['change_time'] = details.getAttribute('change_time')
            book['edition_info'] = details.getAttribute('edition_info')
            book['language'] = details.getAttribute('language')
            book['physical_description_text'] = \
                details.getAttribute('physical_description_text')

            # Cover: get from librarything:
            book['cover'] = get_cover(book['isbn'])

            xml['books'].append(book)

        return xml


def get_cover(isbn):
    from settings import LIBRARYTHINGS_KEY as lkey
    return 'http://covers.librarything.com/devkey/' +\
        lkey + '/medium/isbn/' + isbn
