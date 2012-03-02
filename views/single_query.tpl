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
    <p>Wybierz interesujące cię hasło oraz wersję językową Wikipedii</p>
  </header>
  <br />

  <section id="query" style="overflow: auto; width: 30%;" class="left">
    <form id="query-form">
      <div id="phrase" class="left">
        {{phrase}}:
        <input type="text" id="query-field" class="sep-r">
        <br />
        {{language}}:
        <select name="choose-lang" id="lang-field" class="sep-r">
          <option value="pl">polski</option>
          <option value="en">angielski</option>
          <option value="de">niemiecki</option>
          <option value="fr">francuski</option>
        </select>
      </div>
        <br />
      <div id="query-button" class="left button sep-l">{{query_button}}</div>
    </form>
  </section>

  <section id="results" class="right half">
    <form id="select-phrase">
      {{phrases_title}}:
      <div id="results-propositions">
      </div>
      <div class="left button">{{select_button}}</div>
    </form>
  </section>
  
  <script src="/static/js/jquery-1.7.1.min.js"></script>
  <script src="/static/js/app.js"></script>
  <script src="/static/js/store.js"></script>

  <script type="text/javascript" language="javascript">
  // <![CDATA[
    _app.init();
  // ]]>
  </script>
</body>
</html>
