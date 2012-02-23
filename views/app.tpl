<!DOCTYPE HTML>
<html lang="{{lang}}">
<head>
  <meta charset="UTF-8">
  <title>{{title}}</title>
  <link rel="stylesheet" type="text/css" href="/static/css/style.css"/>
</head>
<body>

  <div id="app">
    <form id="select-mode">
      <input type="radio" name="mode" value="1" checked>{{mode1}}
      <br>
      <input type="radio" name="mode" value="2">{{mode2}}
      <br>
      <button id="select-mode-button" type="button">{{mode_select}}</button>
    </form>
    
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
    
    
    <form id="select-phrase">
      {{phrases_title}}:
      <div id="phrase-propositions">
      </div>
      <button id="select-phrase-button" type="button">{{phrase_select}}</button>
      <input id="fresh-button" type="checkbox" checked>{{fresh_data}}
    </form>
    
    <form id="diagram-results">      
      <div id="diagram">
        DIAGRAM
      </div>
      
      <input type="submit" value="{{save}}">
    </form>
  </div>
  
  <script src="/static/js/jquery-1.7.1.min.js"></script>
  <script src="/static/js/protovis.js"></script>
  <!-- change to minified version in deployment
  <script src="/static/js/protovis.min.js"></script> -->
  <script src="/static/js/app.js"></script>
  <script src="/static/js/diagram.js"></script>
  <script src="/static/js/store.js"></script>

  <script type="text/javascript" language="javascript">
  // <![CDATA[
    _app.init();
  // ]]>
  </script>
</body>
</html>