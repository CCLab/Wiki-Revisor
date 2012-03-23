# -*- coding: utf-8 -*-

from bottle import install, route, run, template, request
import wiki_db as wdb

import simplejson as js
import urllib
import os
file_path = os.path.dirname( __file__ )
db_path = os.path.join( file_path, 'cache.db' )

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

@route('/single_query')
def single_query():
    template_dict = {
        'html_lang'    : 'pl',
        'title'        : 'Znajdź artykuł',
        'phrase'       : 'Hasło',
        'language'     : 'Język',
        'query_button' : 'Szukaj',
        'target_url'   : 'graph'
    }

    return template( 'single_query', template_dict )

@route('/first_query')
def first_query():
    template_dict = {
        'html_lang'    : 'pl',
        'title'        : 'Znajdź artykuł',
        'phrase'       : 'Hasło',
        'language'     : 'Język',
        'query_button' : 'Szukaj',
        'target_url'   : 'second_query'
    }

    return template( 'single_query', template_dict )

@route('/second_query/<lang>/<query>')
def data( db, lang, query ):
    template_dict = {
        'html_lang'    : 'pl',
        'title'        : 'Znajdź artykuł',
        'phrase'       : 'Hasło',
        'language'     : 'Język',
        'query_button' : 'Szukaj',
        'target_url'   : 'graph/%s/%s' % ( lang, query )
    }

    return template( 'single_query', template_dict )

@route('/propositions')
def propositions( db ):
    query = request.query.query
    lang  = request.query.lang

    propositions = wdb.get_query_hits( db, query, lang )

    # TODO do we need this object?
    return { 'propositions': propositions }


@route('/graph/<path:path>')
def data( db, path ):
    params = path.split('/')

    data  = []
    title = ''
    for i in range( len( params ) / 2 ):
        lang  = params[i*2]
        query = urllib.unquote( params[i*2+1] ).decode('utf-8')

        title += "%s :: " % query
        data.append({
            'lang'  : lang,
            'query' : query,
            'data'  : wdb.get_data( db, query, lang )
        })

    template_dict = {
        'html_lang' : 'pl',
        'title'     : title[:-4],
        'data'      : js.dumps( data )
    }

    return template( 'graph', template_dict )


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

@route('/stats')
def stats( db ):
    template_dict = {
        'html_lang' : 'pl',
        'title'     : 'Statystyki',
        'data'      : wdb.get_stats( db )
    }

    return template( 'stats', template_dict )

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

    return "Done sucessfuly"


# create dbs if not exist
wdb.init_db( db_path, drop=False )
run( host='localhost', port=8080 )
