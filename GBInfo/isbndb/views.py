

from isbndb.api import request


"""
Formulario: Un campo con un selector con los valores:
 * Búsqueda rápida (full)
 * ISBN
 * Título
 * Autor
 * Publicador
 * Tópico
"""

URL_DATAS={'book': 'http://isbndb.com/api/books.xml',
           'person_id': 'http://isbndb.com/api/authors.xml',
           'subject_id': 'http://isbndb.com/api/subjects.xml',
           'publisher_id': 'http://isbndb.com/api/publishers.xml'}

def book_search(field, data):
    if 'full' or 'isbn' o 'title' in field:
        books = request(URL_DATAS['book'], dict(index1=field, value1=data))
        return books
    else:
        all_fields_id = request(URL_DATAS[field], dict(index1='name', value1=data))

        results = {'results': 0, 'books': []}
        for field_id in all_fields_id:
            books = request(URL_DATAS['book'], dict(index1=field, value1=field_id))
            results['results'] += books['results']
            for book in books['books']:
                results['books'].append(book)
        return results
