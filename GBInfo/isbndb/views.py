from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.template.loader import render_to_string

from isbndb.api import request
from isbndb.forms import Searcher

URL_DATAS={'book': 'http://isbndb.com/api/books.xml?results=details&',
           'person_id': 'http://isbndb.com/api/authors.xml?results=details&',
           'subject_id': 'http://isbndb.com/api/subjects.xml?results=details&',
           'publisher_id': 'http://isbndb.com/api/publishers.xml?results=details&'}


def book_search(field, data):
    if 'full' or 'isbn' or 'title' in field:
        books = request(URL_DATAS['book'],
                        dict(index1=field, value1=data))

        count = books['results']
        if count > 10:
            if count > 50:
                count=50;
            for i in range(count/10):
                url = URL_DATAS['book'] + 'page_number=' + str(i+2) + '&'
                next_page = request(url, dict(index1=field, value1=data))
                for book in next_page['books']:
                    books['books'].append(book)

        return books['books']

    else:
        all_fields_id = request(URL_DATAS[field],
                                dict(index1='name', value1=data))

        results = {'results': 0, 'books': []}
        for field_id in all_fields_id:
            books = request(URL_DATAS['book'],
                            dict(index1=field, value1=field_id))
            results['results'] += books['results']
            for book in books['books']:
                results['books'].append(book)
        return results['books']


def results(request):
    if request.method == 'POST':
        form = Searcher(request.POST)
        field = form.cleaned_data('search_type')
        data = form.cleaned_data('search_string')
        items = book_search(field, data)
    else:
        form = Searcher()
        items = None

    return request_to_response('isbndb/index.html', {
            'form': form,
            'items': items,
            }, context_instance=RequestContext(request))
