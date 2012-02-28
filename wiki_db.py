# -*- coding: utf-8 -*-

import wiki_api as wapi

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
                               (query_id integer, year integer, month integer, 
                                day integer, time text, author text)
    '''
    create_last_revisions_query = '''create table if not exists last_revisions
                                    (query_id integer, last_revision integer)
    '''
    
    cursor.execute( create_id_map_query )
    cursor.execute( create_search_map_query )
    cursor.execute( create_search_data_query )
    cursor.execute( create_editions_query )
    cursor.execute( create_last_revisions_query )
    

def get_query_hits( db, query, lang ):
    query_id = get_query_id( db, query, lang, table='search_map' )
    db_query = '''select title from search_data
                  where query_id = ?'''
    results = db.execute( db_query, (query_id,) ).fetchall()
    return results if results is None else [t[0] for t in results]

def update_query_hits( db, query, lang ):
    query_id = get_or_create_query_id( db, query, lang, table='search_map' )

    propositions = wapi.search_propositions( query, lang )
    insert_query = '''insert into search_data
                      values (?,?)'''
    for proposition in propositions:
        db.execute( insert_query, (query_id, proposition) )

def is_search_data_cached( db, query, lang ):
    return is_query_cached( db, query, lang, table='search_map' )

def get_data( db, query, lang, year=None, month=None ):
    if is_query_cached( db, query, lang ):
        return get_cached_data( db, query, lang, year, month )
    else:
        return get_fresh_data( db, query, lang, year, month )

def get_cached_data( db, query, lang, year=None, month=None ):
    query_id = get_query_id( db, query, lang )
    
    return {
        'editions': get_editions( db, query_id, year, month )
    }
    
def get_fresh_data( db, query, lang, year=None, month=None ):
    fresh_data = wapi.grab_data( lang, query )
    update_full_data( db, query, lang, fresh_data )
    
    return get_cached_data( db, query, lang, year, month )
    
def update_full_data( db, query, lang, data ):
    user_data = {}
    query_id = get_or_create_query_id( db, query, lang )
    update_editions( db, query_id, data['results'] )
    update_last_revision( db, query_id )

    
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
                      values (?,?,?,?,?,?)'''
    # TODO, TODO!!
    for edition, count in editions.iteritems():
        year_str, month_str = edition.split('-')
        year = int( year_str )
        month = int( month_str )
        import random, string
        for i in range( count ):
            day = random.choice(range(30)) + 1
            author=''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6)) 
            time = year_str + ":" + month_str + ":" + str(day)
            db.execute( insert_query, (query_id, year, month, day, time, author) )
    
def update_last_revision( db, query_id ):
    update_query = '''update last_revisions
                      set last_revision=?
                      where query_id=?'''
    last_revision = 1
    db.execute( update_query, (last_revision, query_id) )
    

def get_last_revision( db, query_id ):
    db_query = '''select last_revision from last_revisions
                  where query_id=?'''
    last_revision = db.execute( db_query, (query_id,) ).fetchone()
    return last_revision if last_revision is None else last_revision[0]

def get_editions( db, query_id, year=None, month=None ):
    editions = []
    if month is not None:
        results = get_month_editions( db, query_id, year, month )
    elif year is not None:
        results = get_year_editions( db, query_id, year )
    else:
        results = get_all_time_editions( db, query_id )

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
        
def is_query_cached( db, query, lang, table='id_map' ):
    id = get_query_id( db, query, lang, table )
    return id is not None
    
