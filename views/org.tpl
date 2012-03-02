<!DOCTYPE HTML>
<html lang="{{lang}}">
<head>
  <meta charset="UTF-8">
  <title>{{title}}</title>
  <link href='http://fonts.googleapis.com/css?family=Exo:300&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
  <link rel="stylesheet" type="text/css" href="/static/css/style.css"/>
</head>
<body>

  <header>
  	<h1>Wiki rewizor</h1>
  </header>
  <br />

  <section>
    <form id="input-phrase">
      <div id="phrase">
        {{phrase}}:
        <input type="text" id="phrase-field">
        <br>
        {{language}}:
        <select name="choose-lang" id="lang-field">
          <option value="pl">polski</option>
          <option value="en">angielski</option>
        </select>
      </div>
      <button id="input-phrase-button" type="button">{{mode_select}}</button>
    </form>
  </section>

  <section style="width: 48%;" class="right">
    <h1><a href="/double">Zestawienie haseł</a></h1>
    <a href="/double"><img src="/static/img/both.png" alt="Historia edycji hasła Copyright na anglojęzycznej Wikipedii" class="left" /></a>
    <p class="right">Ten modół pozwoli zobaczyć szczegółowe statystyki pojedynczego hasła z Wikipedii.</p>
    <div class="right button"><a href="/double">Stwórz zestawienie</a></div>
  </section>

    
    
    <form id="select-phrase">
      {{phrases_title}}:
      <div id="phrase-propositions">
      </div>
      <button id="select-phrase-button" type="button">{{phrase_select}}</button>
      <input id="fresh-button" type="checkbox" checked>{{fresh_data}}
    </form>
    
  <canvas id="paper" width="900" height="600"></canvas>
    <form id="diagram-results">      
      <div id="diagram">
        DIAGRAM
      </div>
      
      <input type="submit" value="{{save}}">
    </form>
  </div>
  
  <script src="/static/js/jquery-1.7.1.min.js"></script>
  <script src="/static/js/protovis.js"></script>
  <script src="/static/js/processing-1.3.6.min.js"></script>
  <!-- change to minified version in deployment
  <script src="/static/js/protovis.min.js"></script> -->
  <script src="/static/js/graph.js"></script>
  <script src="/static/js/app.js"></script>
  <script src="/static/js/diagram.js"></script>
  <script src="/static/js/store.js"></script>

  <script type="text/javascript" language="javascript">
  // <![CDATA[
//    _app.init();
  // ]]>
  </script>
</body>
</html>
