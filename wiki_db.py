# -*- coding: utf-8 -*-

import wiki_update as wup

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
        cursor.execute('''drop table last_revisions''')

    create_id_map_query = '''
        create table if not exists id_map
            (query text, lang text, query_id integer)
    '''
    create_search_map_query = '''
        create table if not exists search_map
            (query text, lang text, query_id integer)
    '''
    create_search_data_query = '''
        create table if not exists search_data
            (query_id integer, title text)
    '''
    create_editions_query = '''
        create table if not exists editions
            (query_id integer, year integer, month integer,
             day integer, time text, author text)
    '''
    create_last_revisions_query = '''
        create table if not exists last_revisions
            (query_id integer, last_revision integer)
    '''

    cursor.execute( create_id_map_query )
    cursor.execute( create_search_map_query )
    cursor.execute( create_search_data_query )
    cursor.execute( create_editions_query )
    cursor.execute( create_last_revisions_query )


def is_search_data_cached( db, query, lang ):
    return is_query_cached( db, query, lang, table='search_map' )

def is_query_cached( db, query, lang, table='id_map' ):
    id = get_query_id( db, query, lang, table )
    return id is not None

def get_query_hits( db, query, lang ):
    if not is_search_data_cached( db, query, lang ):
        wup.update_search_data( db, query, lang )

    query_id = get_query_id( db, query, lang, table='search_map' )
    db_query = '''select title from search_data
                  where query_id = ?'''
    results = db.execute( db_query, (query_id,) ).fetchall()

    return [t[0] for t in results]

def get_data( db, query, lang, year=None, month=None ):
    if not is_query_cached( db, query, lang ):
       wup.update_data( db, query, lang )

    return get_cached_data( db, query, lang, year, month )

def get_cached_data( db, query, lang, year=None, month=None ):
    query_id = get_query_id( db, query, lang )

    # TODO do we really need that extra object?
    #return { 'editions': get_editions( db, query_id, year, month ) }
    return get_editions( db, query_id, year, month )

def get_query_id( db, query, lang, table='id_map' ):
    db_query = '''select query_id from ''' + table + '''
                  where query=? and lang=?'''
    query_id = db.execute( db_query, (query.lower(), lang) ).fetchone()

    #return query_id if query_id is None else query_id[0]
    return query_id[0] if query_id else None

def get_editions( db, query_id, year=None, month=None ):
    editions = []
    '''
    if month is not None:
        results = get_month_editions( db, query_id, year, month )
    elif year is not None:
        results = get_year_editions( db, query_id, year )
    else:
        results = get_all_time_editions( db, query_id )
    '''
    results = get_year_month_editions( db, query_id )

    return results

def get_month_editions( db, query_id, year, month ):
    db_query = '''select day, count(*) from editions
                  where query_id=? and year=? and month=?
                  group by day
                  order by day'''
    results = db.execute( db_query, (query_id, year, month) ).fetchall()
    return map( lambda t: { 'day': t[0], 'count': t[1] }, results )

def get_year_editions( db, query_id, year ):
    db_query = '''select month, count(*) from editions
                  where query_id=? and year=?
                  group by month
                  order by month'''
    results = db.execute( db_query, (query_id, year) ).fetchall()
    return map( lambda t: { 'month': t[0], 'count': t[1] }, results )

def get_all_time_editions( db, query_id ):
    db_query = '''select year, count(*) from editions
                  where query_id=?
                  group by year
                  order by year'''
    results = db.execute( db_query, (query_id,) ).fetchall()
    return map( lambda t: { 'year': t[0], 'count': t[1] }, results )

def get_year_month_editions( db, query_id ):
    db_query = '''select year, month, count(*) from editions
                  where query_id=?
                  group by year, month
                  order by year, month'''
    results = db.execute( db_query, (query_id,) ).fetchall()
    return map( lambda t: { 'year': t[0], 'month': t[1],'count': t[2] }, results )

