<!DOCTYPE HTML>
<html lang="{{html_lang}}">
<head>
  <meta charset="UTF-8">
  <title>{{title}}</title>
  <link href='http://fonts.googleapis.com/css?family=Exo:300&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
  <link rel="stylesheet" type="text/css" href="/static/css/style.css"/>
</head>
<body>

  <header>
      <h1 style="float: left;"><a href="/">Wiki rewizor</a></h1>
      <a href="/">
        <p style="float: right; margin-top: 12px;" class="button">Nowy wykres</p>
      </a>
  </header>
  
  <br />

  <article style="width: 800px; margin: 0px auto; clear: both;">
    <p id="wiki-link-01" class="left"></p>
    <canvas id="paper" width="800" height="600"></canvas>
    <p id="wiki-link-02" class="left"></p>
  </article>
  
  <script src="/static/js/jquery-1.7.1.min.js"></script>
  <script src="/static/js/processing-1.3.6.min.js"></script>
  <script src="/static/js/graph.js"></script>
  <script type="text/javascript" language="javascript">
  // <![CDATA[
      _graph.draw_graph( {{!data}} );
  // ]]>
  </script>
</body>
</html>
