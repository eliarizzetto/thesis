import cerberus
from cerberus import *
import json

csv_schema = {
    "id": {'type': 'number'},
    "title": {
        "error": "is missing"
    },
    "author": {},
    "pub_date": {
        "2013-07":
            {
                "syntax_error":False,
                "format_error": {
                    "boolOt" : False
                    "cose da corregeg" : ""
                }
            }
    },
    "venue": {},
    "volume": {},
    "issue": {},
    "page": {},
    "type": {},
    "publisher": {},
    "editor": {},
}

id_schema = {

}

v = cerberus.Validator
doc = {'id': 'doi:10.1007/978-3-540-88851-2 isbn:9783540888505 isbn:9783540888512', 'title': 'Information Systems " \
      "Outsourcing', 'author': '', 'pub_date': '2009', 'venue': '', 'volume': '', 'issue': '', 'page': '', " \
      "'type': 'book', 'publisher': 'Springer Science and Business Media LLC [crossref:297]', 'editor': 'Hirschheim, " \
      "Rudy; Heinzl, Armin; Dibbern, Jens'}

id_field = {'id': 'doi:10.1007/978-3-540-88851-2 isbn:9783540888505 isbn:9783540888512'}
id_field_content = id_field['id'].split()

ot_prova = v.validate(doc, id_schema)
print(ot_prova)

