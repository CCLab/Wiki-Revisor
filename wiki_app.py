# -*- coding: utf-8 -*-

from bottle import install, route, run, template, request
import wiki_db as wdb

import simplejson as js
import urllib
import os
file_path = os.path.dirname( __file__ )
db_path = os.path.join( file_path, 'tmp', 'test.db' )

from bottle_sqlite import SQLitePlugin
install( SQLitePlugin(dbfile=db_path) )


# To generate html file
template_dict = {
    'mode_select': 'Wybierz',
    'query_button': 'Szukaj',
    'select_button': 'Wybierz',
    'lang': 'pl',
    'title': 'WikiSearch',
    'mode1': 'Sprawdź hasło',
    'mode2': 'Porównaj hasła',
    'phrases_title': 'Dokładne hasła',
    'phrase_select': 'Wybierz hasło',
    'phrase': 'Hasło',
    'language': 'Język',
    'fresh_data': 'Aktualne dane',
    'save': 'Zapisz'
}
# routing

@route('/')
def index():
    return template( 'index', template_dict )

@route('/single')
def single_query():
    return template( 'single_query', template_dict )

@route('/propositions')
def propositions( db ):
    query = request.query.query
    lang  = request.query.lang

    propositions = wdb.get_query_hits( db, query, lang )

    # TODO do we need this object?
    return { 'propositions': propositions }

@route('/data/<lang>/<query>')
def data( db, lang, query ):
    query = urllib.unquote( query ).decode('utf-8')
    data = wdb.get_data( db, query, lang )

    return template( 'single_graph', { 'query': query, 'data': data })

#@route('/data')
#def data( db ):
#    query = request.query.query
#    lang  = request.query.lang
#
#    data = wdb.get_data( db, query, lang )
#
#    return { 'data': data }

@route('/year')
def year_data( db ):
    query = request.query.query
    lang = request.query.lang
    year = request.query.year

    data = wdb.get_year_data( db, query, lang, year )

    return { 'data': data }

@route('/month')
def month_data( db ):
    query = request.query.query
    lang = request.query.lang
    year = request.query.year

    data = wdb.get_month_data( db, query, lang, year, month )

    return { 'data': data }


# static files
from bottle import static_file

@route('/static/css/<filename>')
def server_static(filename):
    return static_file(filename, root='static/css')

@route('/static/img/<filename>')
def server_static(filename):
    return static_file(filename, root='static/img')

@route('/static/js/<filename>')
def server_static(filename):
    return static_file(filename, root='static/js')


#Remove all data from db
#TODO: REMOVE when not needed!!!!!
@route('/purge/')
def purge_db():
    wdb.init_db( db_path, drop=True )


# create dbs if not exist
wdb.init_db( db_path, drop=False )
# start server
run(host='localhost', port=8080, debug=True, reloader=True)


