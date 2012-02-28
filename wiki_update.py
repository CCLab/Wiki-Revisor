# -*- coding: utf-8 -*-

import wiki_api as wapi

def update_query_hits( db, query, lang ):
    query_id = get_or_create_query_id( db, query, lang, table='search_map' )

    propositions = wapi.search_propositions( query, lang )
    insert_query = '''insert into search_data
                      values (?,?)'''
    for proposition in propositions:
        db.execute( insert_query, (query_id, proposition) )

def update_data( db, query, lang ):
    data = wapi.grab_data( lang, query )
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

