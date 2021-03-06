# -*- coding: utf-8 -*-

import urllib as ul
import simplejson as js

DATA_DEBUG = False

def search_propositions( query, lang ):
    host = 'http://'+lang+'.wikipedia.org/w/api.php'
    data = ul.urlencode({
        'action'   : 'query',
        'format'   : 'json',
        'list'     : 'search',
        'srsearch' : query.encode('utf-8')
    })

    if DATA_DEBUG:
        print ">>> %s" % data

    # read stringified json result
    search_results = ul.urlopen( host, data ).read()
    # serialize it as python dictionary
    search_results = js.loads( search_results )
    if DATA_DEBUG:
        print ">>> %s" % search_results

    # due to WikiMedia bug reported here:
    # https://bugzilla.wikimedia.org/show_bug.cgi?id=16572
    while 'error' in search_results.keys():
        if DATA_DEBUG:
            print ">>> Error ocured - I'm trying again!"
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


def grab_data( lang, query, startid=None ):
    host = 'http://'+lang+'.wikipedia.org/w/api.php'
    data = {
        'action'  : 'query',
        'format'  : 'json',
        'titles'  : query.encode('utf-8'),
        'prop'    : 'revisions',
        'rvlimit' : 100,
        'rvdir'   : 'newer'
    }
    if startid:
        data['rvstartid'] = startid

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

    revisions_list   = []
    last_id = None
    while True:
        for page_id in revision_results['query']['pages']:
            for revision in revision_results['query']['pages'][page_id]['revisions']:
                user       = revision.get( 'user', '' )
                date, time = revision['timestamp'].strip('Z').split('T')
                y, m, d = date.split('-')

                revisions_list.append( ( int(y), int(m), int(d), time, user ) )

                last_id = revision['revid']

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

    final_data = {
        'last_id': last_id,
        'results': revisions_list[1:] if startid else revisions_list
    }

    if DATA_DEBUG:
        print ">>> FINAL RESULTS"
        print final_data

    return final_data

