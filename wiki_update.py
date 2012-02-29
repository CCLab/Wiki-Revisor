# -*- coding: utf-8 -*-

import wiki_api as wapi

def update_search_data( db, query, lang ):
    query_id = get_or_create_query_id( db, query, lang, table='search_map' )
    db_query = '''select title from search_data
                  where query_id=?'''
    prev_list = db.execute( db_query, (query_id,) ).fetchall()
    prev_results = {}
    for t in prev_list:
        prev_results[ t ] = True

    propositions = wapi.search_propositions( query, lang )
    new_results = {}
    for t in propositions:
        new_results[ t ] = True

    delete_query = '''delete from search_data
                      where query_id=? and title=?'''
    for title in prev_results:
        if title not in new_results:
            db.execute( delete_query, (query_id,title) )

    insert_query = '''insert into search_data
                      values (?,?)'''
    for title in propositions:
        if title not in prev_results:
            db.execute( insert_query, (query_id,title) )

def update_data( db, query, lang ):
    query_id = get_or_create_query_id( db, query, lang )
    last_id = get_last_revision_id( db, query_id )

    data = wapi.grab_data( lang, query, startid=last_id )

    update_editions( db, query_id, data['results'] )
    update_last_revision( db, query_id, data['last_id'] )

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
    # insert new values
    insert_query = '''insert into editions
                      values (?,?,?,?,?,?)'''
    for t in editions:
        db.execute( insert_query, (query_id, t[0], t[1], t[2], t[3], t[4]) )

def get_last_revision_id( db, query_id ):
    db_query = '''select last_revision from last_revisions
                  where query_id=?'''
    last_id = db.execute( db_query, (query_id,) ).fetchone()
    return None if last_id is None else last_id[0]

def get_last_revision( db, query_id ):
    db_query = '''select last_revision from last_revisions
                  where query_id=?'''
    last_revision = db.execute( db_query, (query_id,) ).fetchone()
    return None if last_revision is None else last_revision[0]

def update_last_revision( db, query_id, last_revision ):
    update_query = '''update last_revisions
                      set last_revision=?
                      where query_id=?'''
    db.execute( update_query, (last_revision, query_id) )

