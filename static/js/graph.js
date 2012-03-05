_graph = (function () {
    var that = {};

    that.draw_graph = function ( data1, query1, data2, query2 ) {

        function sketch( p5 ) {

          p5.setup = function () {
              p5.size( 800, !!data2 ? 700 : 500 );
              p5.noStroke();
              p5.fill( 255, 100 );
              p5.noLoop();
          };

          p5.draw = function() {
              if( !data2 ) {
                  single_graph( data1, query1 );
              }
              else {
                  double_graph( data1, query1, data2, query2 );
              }
          };

          function double_graph ( data1, query1, data2, query2 ) {
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
            var max_count1 = data1.sort( function ( a, b ) { return b['count'] - a['count'] } )[0]['count'];
            var max_count2 = data2.sort( function ( a, b ) { return b['count'] - a['count'] } )[0]['count'];
            var max_count  = Math.max( max_count1, max_count2 );
            var reference  = max_count > 150 ? max_count : 150;

            var years = today.getFullYear() - 2000;

            p5.background( 80 );
            p5.translate( margin_x, margin_y );

            p5.textFont( p5.createFont( 'sans-serif' ), 18 );
            p5.textAlign( p5.CENTER );

            // background annual stripes
            for( i = 0; i < years; ++i ) {
                p5.fill( i % 2 == 0 ? 95 : 100 );
                p5.rect( i * year_width, 0, year_width, height );

                p5.fill( 130 );
                p5.text( 2001 + i, i * year_width + year_width / 2, 30 );
            }

            p5.fill( 190 );
            p5.textAlign( p5.LEFT );
            p5.text( query1, 5, -7 );
            p5.text( query2, 5, height+20 );

            p5.fill( 160 );
            p5.textFont( p5.createFont( 'sans-serif' ), 10 );

            p5.pushMatrix();
            p5.translate( 0, -height * 0.47 );
            data1.forEach( function ( e ) {
                var x = (( e['year'] - 2001 ) * 12 + e['month'] - 1 ) * bar_width;
                var w = bar_width * 0.75;
                var h = height / 2 * 0.88 * ( e['count'] / reference );


                if( max_count1 == e['count'] ) {
                    p5.pushStyle();

                    p5.fill( 255 );
                    p5.stroke( 150 );
                    p5.line( x, height - h, x + w + 30, height - h );
                    p5.text( max_count1, x + w + 3, height - h - 3 );

                    p5.noStroke();
                    p5.rect( x, height, w, -h );

                    p5.popStyle();
                }
                else {
                    p5.rect( x, height, w, -h );
                }
            });

            data2.forEach( function ( e ) {
                var x = (( e['year'] - 2001 ) * 12 + e['month'] - 1 ) * bar_width;
                var w = bar_width * 0.75;
                var h = height / 2 * 0.88 * ( e['count'] / reference );


                if( max_count2 == e['count'] ) {
                    p5.pushStyle();

                    p5.fill( 255 );
                    p5.stroke( 150 );
                    p5.line( x, height + h, x + w + 30, height + h );
                    p5.text( max_count2, x + w + 3, height + h + 11 );

                    p5.noStroke();
                    p5.rect( x, height, w, h );

                    p5.popStyle();
                }
                else {
                    p5.rect( x, height, w, h );
                }
            });

            p5.strokeWeight( 2 );
            p5.stroke( 80 );
            p5.line( 0, height, width, height );

            p5.popMatrix();
          }

          function single_graph ( data, query ) {
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
            var reference  = max_count > 150 ? max_count : 150;

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

          }
        }

        var canvas     = document.getElementById( 'paper' );
        var processing = new Processing( canvas, sketch );
    };

    return that;
})();
