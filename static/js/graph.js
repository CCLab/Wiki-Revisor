_graph = (function () {
    var that = {};

    that.draw_graph = function ( data, query ) {

        function sketch( p5 ) {
          p5.setup = function () {
              p5.size( 800, 500 );
              p5.noStroke();
              p5.fill( 255, 100 );
              p5.noLoop();
              fonts = p5.PFont.list();
              console.log( fonts );
          };

          p5.draw = function() {
            var i;
            var width  = p5.width - 60;
            var height = p5.height - 60;
            var margin_x = 30;
            var margin_y = 30;

            // January, 2001 is the starting point of Wikipedia
            var today      = new Date();
            var bar_num    = ( today.getFullYear() - 2000 ) * 12;
            var bar_width  = width / bar_num;
            var year_width = bar_width * 12;
            var max_count  = data.sort( function ( a, b ) { return b['count'] - a['count'] } )[0]['count'];
            var reference  = max_count > 50 ? max_count : 50;

            var years = today.getFullYear() - 2000;

            p5.background( 80 );
            console.log( margin_x );
            p5.translate( margin_x, margin_y );

            p5.textFont( p5.createFont( 'sans-serif' ), 18 );
            p5.textAlign( p5.CENTER );

            for( i = 0; i < years; ++i ) {
                p5.fill( i % 2 == 0 ? 95 : 100 );
                p5.rect( i * year_width, 0, year_width, height );

                p5.fill( 130 );
                p5.text( 2001 + i, i * year_width + year_width / 2, 30 );
            }

            p5.fill( 190 );
            p5.textAlign( p5.LEFT );
            p5.text( query, 5, -7 );

            p5.fill( 160 );
            p5.textFont( p5.createFont( 'sans-serif' ), 10 );

            data.forEach( function ( e ) {
                var x = (( e['year'] - 2001 ) * 12 + e['month'] - 1 ) * bar_width;
                var w = bar_width * 0.75;
                var h = height * 0.88 * ( e['count'] / reference );


                if( max_count == e['count'] ) {
                    p5.pushStyle();

                    p5.fill( 255 );
                    p5.stroke( 150 );
                    p5.line( x, height - h, x + w + 30, height - h );
                    p5.text( max_count, x + w + 3, height - h - 3 );

                    p5.noStroke();
                    p5.rect( x, height, w, -h );

                    p5.popStyle();
                }
                else {
                    p5.rect( x, height, w, -h );
                }
            });
          };
        }

        var canvas     = document.getElementById( 'paper' );
        var processing = new Processing( canvas, sketch );
    };

    return that;
})();
