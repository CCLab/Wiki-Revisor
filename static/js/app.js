_app = (function (){
    var that = {};

    that.init = function() {
        $('#results').hide();

        $('#query-button').click( function () {
            $('#query-form').submit();
        });

        $('#query-form').submit( function () {
            var query = $('#query-field').val();
            var lang  = $('#lang-field').val();
            state.add_lang( lang );

            $('#results').fadeOut( 25 );

            _store.get_propositions( query, lang, show_propositions );

            return false;
        });
    };

    function show_propositions( data ) {
        var propositions = data['propositions'];
        var results_prop = $('#results-propositions');
        var lang = $('#lang-field').val();

        // remove previously displayed results
        results_prop.empty();

        // add new results
        results_prop.append( propositions.map( function ( e ) {
            return '<li>' +
                     '<a href="/single_graph/'+ lang +'/'+ encodeURIComponent( e ) +'">' +
                       '<p class="button">' + e +'</p>' +
                     '</a>' +
                   '</li>';
        }).join( '' ) );

        // show results
        $('#results').fadeIn( 250 );
    }

//    function draw_diagram() {
//        var full_data = state.get_data();
//        var image_width = 600;
//        var image_height = 400;
//        var merged_data = [];
//        var mode = state.get_mode();
//
//        // if not all data is downloaded
//        if ( full_data.length < mode ) {
//            return;
//        }
//
//        $('#select-phrase').hide();
//        $('#diagram-results').show();
//
//        merged_data = merge_data( full_data );
//
//        //_diagram.draw( merged_data, mode, image_width, image_height );
//        $('#paper').show();
//        _graph.draw_graph( full_data[0]['editions'], state.get_query( 0 ) );
//    }
//
//
//    function arm_buttons() {
//        $('.single').click( function () {
//            state.set_mode( 1 );
//
//            $('#input-phrase').show();
//            $('#phrase-field').val('');
//            $('#select-mode').hide();
//        });
//
//
//        $('#select-mode-button').click( function() {
//            var mode = $('#select-mode').find('input:checked').val();
//
//            state.set_mode( parseInt( mode, 10 ) );
//
//            $('#input-phrase').show();
//            $('#phrase-field').val('');
//            $('#select-mode').hide();
//        });
//
//        $('#input-phrase-button').click( function() {
//            $('#input-phrase').submit();
//        });
//
//        $('#input-phrase').submit( function() {
//            var phrase = $(this).find('#phrase-field').val();
//            var lang = $(this).find('#lang-field').val();
//            state.add_lang( lang );
//
//            _store.get_propositions( phrase, lang, show_propositions );
//
//            return false;
//        });
//
//        $('#select-phrase-button').click( function() {
//            $('#select-phrase').submit();
//        });
//
//        $('#select-phrase').submit( function() {
//            var query = $(this).find('input:checked').val();
//            var lang = state.get_lang( state.act_nr() );
//
//            state.add_query( query );
//
//            get_data( query, lang, try_draw_diagram );
//
//            if ( state.get_mode() > state.act_nr() ) {
//                $('#input-phrase').show();
//                $('#select-phrase').hide();
//            }
//
//
//            return false;
//        });
//    }
//
//

    function get_data( query, lang, callback ) {
        function response( received_data ) {
            state.add_data( received_data );
            callback();
        }

        var fresh_data = $('#fresh-button').is(':checked');

        if ( fresh_data ) {
            _store.get_fresh_data( query, lang, response );
        } else {
            _store.get_cached_data( query, lang, response );
        }
    }


    function merge_data( full_data ) {
        function cmp_dates( date1, date2 ) {
            function date_to_value( date ) {
                return 12 * date['year'] + date['month'];
            }
            return date_to_value( date1 ) - date_to_value( date2 );
        }
        function next_date( date ) {
            if ( date['month'] === 12 ) {
                return {
                    'month': 1,
                    'year' : date['year'] + 1
                };
            } else {
                return {
                    'month': date['month'] + 1,
                    'year' : date['year']
                };
            }
        }
        function create_clean_object( date, sources_number ) {
            var obj = {
                'month': date['month'],
                'year' : date['year'],
                'time' : date['year'] + '-' + date['month']
            };
            var i;
            var key;
            for ( i = 1; i <= sources_number; ++i ) {
                key = 'changes' + i;
                obj[ key ] = 0;
            }

            return obj;
        }

        var min_date = full_data.map( function ( data ) {
            return data['editions'][0];
        }).sort( cmp_dates )[0];
        var max_dates = full_data.map( function ( data ) {
            return data['editions'][ data['editions'].length - 1 ];
        }).sort( cmp_dates );
        var max_date = max_dates[ max_dates.length - 1 ];

        var act_date = min_date;
        var merged_data = [];
        while ( cmp_dates( act_date, max_date ) <= 0 ) {
            merged_data.push( create_clean_object( act_date, full_data.length ) );
            act_date = next_date( act_date );
        }

        full_data.forEach( function ( data, i ) {
            var editions = data['editions'];
            var key = 'changes' + (i+1);
            var ind = 0;
            merged_data.forEach( function ( e ) {
                if ( ind < editions.length && !cmp_dates( editions[ ind ], e ) ) {
                    e[ key ] = editions[ ind ][ 'count' ];
                    ind += 1;
                }
            });
        });

        // TODO: last changes are lost
        return merged_data;
    }

    var state = (function() {
        var _langs = [];
        var _queries = [];
        var _mode;
        var _data = [];

        return {
            reset: function() {
                _langs = [];
                _queries = [];
                _data = [];
            },
            act_nr: function() {
                return _queries.length;
            },
            set_mode: function( mode ) {
                _mode = mode;
            },
            get_mode: function() {
                return _mode;
            },
            add_lang: function( lang ) {
                _langs.push( lang );
            },
            add_query: function( query ) {
                _queries.push( query );
            },
            get_lang: function( nr ) {
                return _langs[ nr ];
            },
            get_query: function( nr ) {
                return _queries[ nr ];
            },
            add_data: function( data ) {
                _data.push( data );
            },
            get_data: function() {
                return _data;
            }
        };
    })();

    return that;
})();
