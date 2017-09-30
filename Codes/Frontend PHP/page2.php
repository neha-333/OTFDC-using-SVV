<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Theme Made By www.w3schools.com - No Copyright -->
  <title>proKnap Search Engine</title>
  <link rel="shortcut icon" type="image/png" href="logo.png">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet" type="text/css">
  <link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet" type="text/css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script src="//code.jquery.com/jquery-2.1.4.min.js"></script>
  <script src="waterbubble.js"></script>

  <style>
  body {
      font: 400 15px Lato, sans-serif;
      line-height: 1.8;
      color: #818181;
  }

  p {
	margin-bottom:0px;
	font-size:11pt;
  }

  h1{
	margin-top:0px;
	margin-bottom:10px;
	display:inline;
  }

  img{
	display:inline;
	margin-bottom:20px;
  }

  h2 {
      font-size: 24px;
      text-transform: uppercase;
      color: #303030;
      font-weight: 600;
      margin-bottom: 30px;
  }
  h3{

      margin-bottom: 0px;
  }
  h4 {
      font-size: 19px;
      line-height: 1.375em;
      color: #303030;
      font-weight: 400;
      margin-bottom: 30px;
  }
  .jumbotron {
      background-color: #f4511e;
      color: #fff;
      padding: 10px 10px;
      font-family: Montserrat, sans-serif;
  }
  .container-fluid {
      padding: 60px 50px;
  }
  .bg-grey {
      background-color: #f6f6f6;
  }
  .logo-small {
      color: #f4511e;
      font-size: 50px;
  }
  .logo {
      color: #f4511e;
      font-size: 200px;
  }
  .thumbnail {
      padding: 0 0 15px 0;
      border: none;
      border-radius: 0;
  }
  .thumbnail img {
      width: 100%;
      height: 100%;
      margin-bottom: 10px;
  }
  .carousel-control.right, .carousel-control.left {
      background-image: none;
      color: #f4511e;
  }
  .carousel-indicators li {
      border-color: #f4511e;
  }
  .carousel-indicators li.active {
      background-color: #f4511e;
  }
  .item h4 {
      font-size: 19px;
      line-height: 1.375em;
      font-weight: 400;
      font-style: italic;
      margin: 10px 0;
  }
  .item span {
      font-style: normal;
  }
  .panel {
      border: 1px solid #f4511e;
      border-radius:0 !important;
      transition: box-shadow 0.5s;
  }
  .panel:hover {
      box-shadow: 5px 0px 40px rgba(0,0,0, .2);
  }
  .panel-footer .btn:hover {
      border: 1px solid #f4511e;
      background-color: #fff !important;
      color: #f4511e;
  }
  .panel-heading {
      color: #fff !important;
      background-color: #f4511e !important;
      padding: 25px;
      border-bottom: 1px solid transparent;
      border-top-left-radius: 0px;
      border-top-right-radius: 0px;
      border-bottom-left-radius: 0px;
      border-bottom-right-radius: 0px;
  }
  .panel-footer {
      background-color: white !important;
  }
  .panel-footer h3 {
      font-size: 32px;
  }
  .panel-footer h4 {
      color: #aaa;
      font-size: 14px;
  }
  .panel-footer .btn {
      margin: 15px 0;
      background-color: #f4511e;
      color: #fff;
  }

  .navbar {
      margin-bottom: 0;
      background-color: #f4511e;
      z-index: 9999;
      border: 0;
      font-size: 12px !important;
      line-height: 1.42857143 !important;
      letter-spacing: 4px;
      border-radius: 0;
      font-family: Montserrat, sans-serif;
  }
  .navbar li a, .navbar .navbar-brand {
      color: #fff !important;
  }
  .navbar-nav li a:hover, .navbar-nav li.active a {
      color: #f4511e !important;
      background-color: #fff !important;
  }
  .navbar-default .navbar-toggle {
      border-color: transparent;
      color: #fff !important;
  }
  footer .glyphicon {
      font-size: 20px;
      margin-bottom: 20px;
      color: #f4511e;
  }
  .slideanim {visibility:hidden;}
  .slide {
      animation-name: slide;
      -webkit-animation-name: slide;
      animation-duration: 1s;
      -webkit-animation-duration: 1s;
      visibility: visible;
  }
  @keyframes slide {
    0% {
      opacity: 0;
      transform: translateY(70%);
    }
    100% {
      opacity: 1;
      transform: translateY(0%);
    }
  }
  @-webkit-keyframes slide {
    0% {
      opacity: 0;
      -webkit-transform: translateY(70%);
    }
    100% {
      opacity: 1;
      -webkit-transform: translateY(0%);
    }
  }
  @media screen and (max-width: 768px) {
    .col-sm-4 {
      text-align: center;
      margin: 25px 0;
    }
    .btn-lg {
        width: 100%;
        margin-bottom: 35px;
    }
  }
  @media screen and (max-width: 480px) {
    .logo {
        font-size: 150px;
    }
  }

  .results{
	margin-left:140px;
	margin-bottom:0;
	width:740px;
  }
  </style>

</head>
<body id="myPage" data-spy="scroll" data-target=".navbar" data-offset="60" >
  <?php $k = $_POST['query'] ?>
  <div class="jumbotron text-center">
    <span>
      <h1>pr</h1><img src="logo.png" height=40px width=40px><h1>Knap</h1>
    </span>
    <p style="margin-bottom:0px">Search The Smart Way</p>
    <form class="form-inline" action=page2.php method=POST>
      <input name="query" type="text" class="form-control" size="50" value= "<?php echo $k ?>" required>
      <button type="submit" class="btn btn-danger">Go!</button>
    </form>
  </div>
  <script src="canvasjs.min.js"></script>
  <script type="text/javascript">
		function my(arg,ry,rb,rask,raol) {
      if(ry == 0)
        ry = 11
      if(rb == 0)
        rb = 11
      if(rask == 0)
        rask = 11
      if(raol == 0)
        raol = 11
			var chart = new CanvasJS.Chart("chartContainer".concat(arg), {
				title: {
					text: "Ranks"
				},
				animationEnabled: true,
        axisY: {
				interval: 11
			  },
				data: [
				{
					type: "bar",
					dataPoints: [
					{ x: 1, y: 11-ry, label:"Yahoo"},
					{ x: 2, y: 11-rb, label:"Bing"},
					{ x: 3, y: 11-rask, label:"Ask" },
					{ x: 4, y: 11-raol, label:"Aol" }
					]
				}
				]
			});

			chart.render();
		}
	</script>

  <?php

  $q=$_POST['query'];
  $q=str_replace(' ', '%20', $q);
  $command = escapeshellcmd('/home/karan/svv/rebingscrapy/otfdc.py '.$q);
  shell_exec($command);
  $db = new mysqli('localhost', 'root');
  	if ($db->connect_errno) {
  	echo 'Connect failed: '.$db->connect_error;
  	exit();
  	}
  	$db->select_db('svvtest');
  	$cursor = $db->query("SELECT * FROM result ORDER BY weight DESC");
  	if ($db->error) {
  	echo $db->error.PHP_EOL;
  	}
    $demo=1;
    echo "<table style='margin-left:100px;margin-right:100px'>";

  	while($val = $cursor->fetch_assoc()){
      $rel=$val['vote_distr']*100;
      $rel1=$rel/100;
      if ($val['relevance']==1) {
        $col="#2DA175";
      }
      elseif ($val['relevance']==0.5) {
        $col="#FFC300";
      }
      else {
        $col="#DF2929";
      }
      $i=intval($rel);
      echo "<tr>";
        echo "<td>";
          echo"<canvas id='karan$demo' style='margin: 25px; margin-top:35px'></canvas>";
          echo"<script>
            $('#karan$demo').waterbubble({

            // bubble size
            radius: 30,

            // data to present
            data: $rel1,

            // color of the water bubble
            waterColor: '$col' ,

            // text color
            textColor: 'black',

            // show wave
            wave: true,
            txt: '$i%',
            // enable water fill animation
            animation: true

          });
          </script>";

        echo "</td>";
    		echo "<td>";
        echo "<h3><a href=".$val['link'].">".$val['title']."</a></h3>";
    		echo "<span style='color:green;font-size:12pt;'>".$val['link']."</span>";
    		echo "<p>".$val['description']."</p>";
    		echo "</td>";
        echo "<td >";
        $ry=$val['ranky'];
        $rb=$val['rankb'];
        $rask=$val['rankask'];
        $raol=$val['rankaol'];
        echo"<div id='chartContainer$demo' style='height: 125px; width: 300px;'>
        </div> <script type='text/javascript'> my($demo,$ry,$rb,$rask,$raol) </script>";
        echo "</td>";
        $demo=$demo+1;
  		echo "</tr>";
  	}
    echo "</table>";

  ?>
  </div>
</body>
