# -*- coding: utf-8 -*-

from bottle import install, route, run, template, request
import urllib as ul
import simplejson as js

DATA_DEBUG = False

import os
file_path = os.path.dirname( __file__ )
db_path = os.path.join( file_path, 'tmp', 'test.db' )

from bottle_sqlite import SQLitePlugin
install( SQLitePlugin(dbfile=db_path) )

# routing

@route('/hello/:name')
def index(name='World'):
    return '<b>Hello %s!</b>' % name

@route('/')
def app():
    return template('app', template_dict)
    
@route('/propositions')
def propositions( db ):
    query = request.query.query
    lang = request.query.lang
    
    if not is_search_data_cached( db, query, lang):
        update_query_hits( db, query, lang )
    propositions = get_query_hits( db, query, lang )

    return {
        'propositions': propositions,
        'cached'      : False
    }
    
@route('/data')
def data( db ):
    query = request.query.query
    lang = request.query.lang
    
    data = get_data( db, query, lang )
        
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


#TODO: REMOVE !!!!!
@route('/purge/')
def purge_db():
    init_db( db_path, drop=True )
    
# create tables if any is missing, if drop is True, then drop all tables
def init_db( path, drop=False ):
    import sqlite3
    conn = sqlite3.connect( path )
    cursor = conn.cursor()
    
    if drop:
        print 'Droping tables!'
        cursor.execute('''drop table id_map''')
        cursor.execute('''drop table search_map''')
        cursor.execute('''drop table search_data''')
        cursor.execute('''drop table editions''')
        cursor.execute('''drop table last_editions''')
    
    create_id_map_query = '''create table if not exists id_map
                          (query text, lang text, query_id integer)
    '''
    create_search_map_query = ''' create table if not exists search_map
                                  (query text, lang text, query_id integer)
    '''
    create_search_data_query = '''create table if not exists search_data
                                  (query_id integer, title text)
    '''
    create_editions_query = '''create table if not exists editions
                               (query_id integer, year integer, month integer, count integer)
    '''
    create_last_editions_query = '''create table if not exists last_editions
                                    (query_id integer, last text)
    '''
    
    cursor.execute( create_id_map_query )
    cursor.execute( create_search_map_query )
    cursor.execute( create_search_data_query )
    cursor.execute( create_editions_query )
    cursor.execute( create_last_editions_query )
    
init_db( db_path, drop=False )
#init_db( db_path, drop=True )

# start server
run(host='localhost', port=8080, debug=True, reloader=True)


# DB

def get_query_hits( db, query, lang ):
    query_id = get_query_id( db, query, lang, table='search_map' )
    db_query = '''select title from search_data
                  where query_id = ?'''
    results = db.execute( db_query, (query_id,) ).fetchall()
    return results if results is None else [t[0] for t in results]

def update_query_hits( db, query, lang ):
    query_id = get_or_create_query_id( db, query, lang, table='search_map' )

    propositions = search_propositions( query, lang )
    insert_query = '''insert into search_data
                      values (?,?)'''
    for proposition in propositions:
        db.execute( insert_query, (query_id, proposition) )

def is_search_data_cached( db, query, lang ):
    return is_query_cached( db, query, lang, table='search_map' )

def get_data( db, query, lang ):
    if is_query_cached( db, query, lang ):
        return get_cached_data( db, query, lang )
    else:
        return get_fresh_data( db, query, lang )

def get_cached_data( db, query, lang ):
    query_id = get_query_id( db, query, lang )
    
    return {
        'last'    : get_last_edition( db, query_id ),
        'editions': get_editions( db, query_id )
    }
    
def get_fresh_data( db, query, lang ):
    fresh_data = grab_data( lang, query )
    update_full_data( db, query, lang, fresh_data )
    
    return get_cached_data( db, query, lang )
    
def update_full_data( db, query, lang, data ):
    user_data = {}
    query_id = get_or_create_query_id( db, query, lang )
    update_editions( db, query_id, data['results'] )
    update_last_edition( db, query_id )

    
def get_query_id( db, query, lang, table='id_map' ):
    db_query = '''select query_id from ''' + table + ''' 
                  where query=? and lang=?'''
    query_id = db.execute( db_query, (query, lang) ).fetchone()
    
    return query_id if query_id is None else query_id[0]
    
def get_or_create_query_id( db, query, lang, table='id_map' ):
    query_id = get_query_id( db, query, lang, table )
    if query_id is None:
        new_query_id = get_max_query_id( db, table ) + 1
        db_query = '''insert into ''' + table + ''' 
                      values (?,?,?)'''
        db.execute( db_query, (query, lang, new_query_id) )
        return new_query_id
    else:
        return query_id
        
def get_max_query_id( db, table='id_map' ):
    min_id = 0
    db_query = '''select query_id from ''' + table
    ids = db.execute( db_query, () ).fetchall()

    last_max_id = min_id
    for t in ids:
        last_max_id = max( last_max_id, t[0] )
    return last_max_id
    
def update_editions( db, query_id, editions ):
    # remove old values
    del_query = '''delete from editions
                   where query_id=?'''
    db.execute( del_query, (query_id,) )
    
    # insert new values
    insert_query = '''insert into editions
                      values (?,?,?,?)'''
    for edition, count in editions.iteritems():
        year_str, month_str = edition.split('-')
        year = int( year_str )
        month = int( month_str )
        db.execute( insert_query, (query_id, year, month, count) )
    
def update_last_edition( db, query_id ):
    update_query = '''update last_editions
                      set last=?
                      where query_id=?'''
    act_time = '2012-02-12:13:20:59'
    db.execute( update_query, (act_time, query_id) )
    

def get_last_edition( db, query_id ):
    db_query = '''select last from last_editions
                  where query_id=?'''
    last_time = db.execute( db_query, (query_id,) ).fetchone()
    return last_time if last_time is None else last_time[0]

def get_editions( db, query_id ):
    editions = []
    db_query = '''select year, month, count from editions
                  where query_id=?'''
    results = db.execute( db_query, (query_id,) ).fetchall()
    for t in results:
        editions.append({
            'year': t[0],
            'month': t[1],
            'count': t[2]
        })
    
    # sort by date
    return sorted( editions, key=lambda t: 12*t['year'] + t['month'] )
    
def is_query_cached( db, query, lang, table='id_map' ):
    id = get_query_id( db, query, lang, table )
    return id is not None
    
# Getting data from wikipedia

def search_propositions( query, lang ):
    host = 'http://'+lang+'.wikipedia.org/w/api.php'
    data = ul.urlencode({
        'action'   : 'query',
        'format'   : 'json',
        'list'     : 'search',
        'srsearch' : query.encode('utf-8')
    })

    # read stringified json result
    search_results = ul.urlopen( host, data ).read()
    # serialize it as python dictionary
    search_results = js.loads( search_results )

    # due to WikiMedia bug reported here:
    # https://bugzilla.wikimedia.org/show_bug.cgi?id=16572
    while 'error' in search_results.keys():
        # read stringified json result
        search_results = ul.urlopen( host, data ).read()
        # serialize it as python dictionary
        search_results = js.loads( search_results )

    # print search sugestions
    if DATA_DEBUG:
        print ">>> SEARCH RESULTS"
        print search_results
        # se_res = js.dumps(search_results, encoding='utf-8', sort_keys=True, indent=4)
        # f = open( 'se_res.json', 'wb')
        # f.write( se_res )
        # f.close()


    return [ hit['title'] for hit in search_results['query']['search'] ]
    

def grab_data( lang, hit ):
    host = 'http://'+lang+'.wikipedia.org/w/api.php'
    data = {
        'action'  : 'query',
        'format'  : 'json',
        'titles'  : hit.encode('utf-8'),
        'prop'    : 'revisions',
        'rvlimit' : 100
    }

    # stringify data into GET params
    params = ul.urlencode( data )

    # read stringified json result
    revision_results = ul.urlopen( host, params ).read()
    # serialize it as python dictionary
    revision_results = js.loads( revision_results )

    # print revision sugestions
    if DATA_DEBUG:
        print ">>> REVISION RESULTS"
        print revision_results
        # rev_res = js.dumps(revision_results, encoding='utf-8', sort_keys=True, indent=4)
        # f = open( 'rev_res.json', 'wb')
        # f.write( rev_res )
        # f.close()

    revision_dates = {}
    while True:
        for page_id in revision_results['query']['pages']:
            for revision in revision_results['query']['pages'][page_id]['revisions']:
                d = revision['timestamp'].split('T')[0].rsplit('-',1)[0]
                revision_dates[ d ] = revision_dates.get( d, 0 ) + 1

        if 'query-continue' not in revision_results:
            break

        next_rev = str(revision_results['query-continue']['revisions']['rvstartid'])

        # update the results offset
        data.update({ 'rvstartid': next_rev })

        # stringify data into GET parameters
        params = ul.urlencode( data )
        # read revisions data in json string
        json_data = ul.urlopen( host, params ).read()
        # serialize it as a python dictionary
        revision_results = js.loads( json_data )

    return { 'query': hit, 'results': revision_dates }
    
    
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
