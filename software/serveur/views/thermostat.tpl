<!-- pikaday is from https://github.com/dbushell/Pikaday -->
<html>
<head>
	<title>Gestion de la température</title>
	<meta http-equiv="refresh" content="60;url=thermostat.html?date={{date}}" />
	<link type="text/css" href="style-solarized.css" rel="stylesheet" />
	<link type="text/css" href="pikaday.css" rel="stylesheet" />
</head>
<body>
	<h1>Températures</h1>
	<table>
		<tr>
		<td>Température actuelle&nbsp;:&nbsp;</td>
		<td>{{temp}}&nbsp;°C</td>
		</tr>
	</table>
	<p>L'objectif de température actuel est de {{obj}}&nbsp;°C.</p>
	<h1>Programmation du {{date}}</h1>
	<button id="datepicker">Choisir la date</button>
	<br /><br />
	<form action="/thermostat-prog.html" method="post">
		<table class="prog">
        %def algo(code):
        %   a = (2100 - (((80 - int(ord(code))) * 100) / 2)) / 100
        %   return a
        %end
		%h0, h1, h2, h3, h4, h5 = algo(prog[0]), algo(prog[1]), algo(prog[2]), algo(prog[3]), algo(prog[4]), algo(prog[5])
		%h6, h7, h8, h9, h10, h11 = algo(prog[6]), algo(prog[7]), algo(prog[8]), algo(prog[9]), algo(prog[10]), algo(prog[11])
		%h12, h13, h14, h15, h16, h17 = algo(prog[12]), algo(prog[13]), algo(prog[14]), algo(prog[15]), algo(prog[16]), algo(prog[17])
		%h18, h19, h20, h21, h22, h23 = algo(prog[18]), algo(prog[19]), algo(prog[20]), algo(prog[21]), algo(prog[22]), algo(prog[23])
			<tr>
			<td>0h</td><td>1h</td><td>2h</td><td>3h</td><td>4h</td><td>5h</td><td>6h</td><td>7h</td><td>8h</td><td>9h</td><td>10h</td><td>11h</td>
			</tr>
			<tr>
            	<td><input name="prog_h0" type="text" size="4" value="{{h0}}" /></td>
				<td><input name="prog_h1" type="text" size="4" value="{{h1}}" /></td>
				<td><input name="prog_h2" type="text" size="4" value="{{h2}}" /></td>
				<td><input name="prog_h3" type="text" size="4" value="{{h3}}" /></td>
				<td><input name="prog_h4" type="text" size="4" value="{{h4}}" /></td>
				<td><input name="prog_h5" type="text" size="4" value="{{h5}}" /></td>
				<td><input name="prog_h6" type="text" size="4" value="{{h6}}" /></td>
				<td><input name="prog_h7" type="text" size="4" value="{{h7}}" /></td>
				<td><input name="prog_h8" type="text" size="4" value="{{h8}}" /></td>
				<td><input name="prog_h9" type="text" size="4" value="{{h9}}" /></td>
				<td><input name="prog_h10" type="text" size="4" value="{{h10}}" /></td>
				<td><input name="prog_h11" type="text" size="4" value="{{h11}}" /></td>
            </tr>
			<tr>
				<td>12h</td><td>13h</td><td>14h</td><td>15h</td><td>16h</td><td>17h</td><td>18h</td><td>19h</td><td>20h</td><td>21h</td><td>22h</td><td>23h</td>
			</tr>
			<tr>
				<td><input name="prog_h12" type="text" size="4" value="{{h12}}" /></td>
				<td><input name="prog_h13" type="text" size="4" value="{{h13}}" /></td>
				<td><input name="prog_h14" type="text" size="4" value="{{h14}}" /></td>
				<td><input name="prog_h15" type="text" size="4" value="{{h15}}" /></td>
				<td><input name="prog_h16" type="text" size="4" value="{{h16}}" /></td>
				<td><input name="prog_h17" type="text" size="4" value="{{h17}}" /></td>
				<td><input name="prog_h18" type="text" size="4" value="{{h18}}" /></td>
				<td><input name="prog_h19" type="text" size="4" value="{{h19}}" /></td>
				<td><input name="prog_h20" type="text" size="4" value="{{h20}}" /></td>
				<td><input name="prog_h21" type="text" size="4" value="{{h21}}" /></td>
				<td><input name="prog_h22" type="text" size="4" value="{{h22}}" /></td>
				<td><input name="prog_h23" type="text" size="4" value="{{h23}}" /></td>
            </tr>
		</table>
		<br />
		<input name="date" type="hidden" value="{{date}}" />
		<input class="bouton" value="Programmer la journée" type="submit" />
	</form>
	<h1>Historique de cette journée</h1>
	% t0 = abs((h0 * 10) - 300)
	% t1 = abs((h1 * 10) - 300)
	% t2 = abs((h2 * 10) - 300)
	% t3 = abs((h3 * 10) - 300)
	% t4 = abs((h4 * 10) - 300)
	% t5 = abs((h5 * 10) - 300)
	% t6 = abs((h6 * 10) - 300)
	% t7 = abs((h7 * 10) - 300)
	% t8 = abs((h8 * 10) - 300)
	% t9 = abs((h9 * 10) - 300)
	% t10 = abs((h10 * 10) - 300)
	% t11 = abs((h11 * 10) - 300)
	% t12 = abs((h12 * 10) - 300)
	% t13 = abs((h13 * 10) - 300)
	% t14 = abs((h14 * 10) - 300)
	% t15 = abs((h15 * 10) - 300)
	% t16 = abs((h16 * 10) - 300)
	% t17 = abs((h17 * 10) - 300)
	% t18 = abs((h18 * 10) - 300)
	% t19 = abs((h19 * 10) - 300)
	% t20 = abs((h20 * 10) - 300)
	% t21 = abs((h21 * 10) - 300)
	% t22 = abs((h22 * 10) - 300)
	% t23 = abs((h23 * 10) - 300)
	<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="720" height="220">
		<line x1="0" y1="200" x2="720" y2="200" stroke-width="2" stroke="rgb(38,139,210)" />
		<line x1="0" y1="200" x2="0" y2="0" stroke-width="2" stroke="rgb(38,139,210)" />
		<polyline points="0,200 0,{{t0}} 30,{{t0}} 30,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="30,200 30,{{t1}} 60,{{t1}} 60,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="60,200 60,{{t2}} 90,{{t2}} 90,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="90,200 90,{{t3}} 120,{{t3}} 120,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="120,200 120,{{t4}} 150,{{t4}} 150,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="150,200 150,{{t5}} 180,{{t5}} 180,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="180,200 180,{{t6}} 210,{{t6}} 210,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="210,200 210,{{t7}} 240,{{t7}} 240,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="240,200 240,{{t8}} 270,{{t8}} 270,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="270,200 270,{{t9}} 300,{{t9}} 300,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="300,200 300,{{t10}} 330,{{t10}} 330,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="330,200 330,{{t11}} 360,{{t11}} 360,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="360,200 360,{{t12}} 390,{{t12}} 390,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="390,200 390,{{t13}} 420,{{t13}} 420,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="420,200 420,{{t14}} 450,{{t14}} 450,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="450,200 450,{{t15}} 480,{{t15}} 480,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="480,200 480,{{t16}} 510,{{t16}} 510,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="510,200 510,{{t17}} 540,{{t17}} 540,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="540,200 540,{{t18}} 570,{{t18}} 570,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="570,200 570,{{t19}} 600,{{t19}} 600,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="600,200 600,{{t20}} 630,{{t20}} 630,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="630,200 630,{{t21}} 660,{{t21}} 660,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="660,200 660,{{t22}} 690,{{t22}} 690,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		<polyline points="690,200 690,{{t23}} 720,{{t23}} 720,200" fill="#93a1a1" stroke-width="1" stroke="#586e75" />
		{{!courbe}}
	</svg>
	<script src="moment.min.js"></script>
	<script src="pikaday.js"></script>
	<script>

     // You can get and set dates with moment objects
     var picker = new Pikaday(
     {
         field: document.getElementById('datepicker'),
         firstDay: 0,
         minDate: new Date('2014-01-01'),
         maxDate: new Date('2016-12-31'),
         yearRange: [2014,216],
         onSelect: function() {
             var date = this.getMoment().format('DD-MM-YYYY');
             window.location = 'thermostat.html?date=' + date;
         }
     });
    
     //picker.setMoment(moment().dayOfYear(366));
    
    </script>
	<div class="footer">Dernière mise à jour : {{heure}}</div>
</body>
</html>
