# -*- coding: utf-8 -*-

from bottle import install, route, run, template, request
import wiki_db as wdb

import os
file_path = os.path.dirname( __file__ )
db_path = os.path.join( file_path, 'tmp', 'test.db' )

from bottle_sqlite import SQLitePlugin
install( SQLitePlugin(dbfile=db_path) )


# routing

@route('/')
def app():
    return template('app', template_dict)
    
@route('/propositions')
def propositions( db ):
    query = request.query.query
    lang = request.query.lang
    
    if not wdb.is_search_data_cached( db, query, lang):
        wdb.update_query_hits( db, query, lang )
    propositions = wdb.get_query_hits( db, query, lang )

    return {
        'propositions': propositions,
        'cached'      : False
    }
    
@route('/data')
def data( db ):
    query = request.query.query
    lang = request.query.lang
    
    data = wdb.get_data( db, query, lang )
        
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


# To generate html file
template_dict = {
    'mode_select': 'Wybierz',
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
