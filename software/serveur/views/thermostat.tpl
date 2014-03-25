<html>
<head>
	<title>Gestion de la température</title>
	<meta http-equiv="refresh" content="60;url=thermostat.html">
	<style type="text/css">
		body {
			text-align: center;
			font-family: "Georgia", serif;
			background-color: #FCF6CF;
		}
		h1 {
			font-size: 250%;
		}
		table {
			margin-left: auto;
			margin-right: auto;
			border: 0px;
			font-size: 150%;
		}
		p {
			font-size: 150%;
		}
		.footer {
			font-size: 90%;
			position: absolute;
			bottom: 0px;
			right: 0px;
			height: 1.5em;
		}
		.prog {
			font-size: 150%;
			border-width: 2px;
			border-style: solid;
		}
		.prog td {
			border-width: 1px;
			border-style: solid;
			text-align: center;
		}
		input {
			font-family: "Courier", monospace;
			font-weight: bold;
			font-size: 90%;
			background-color: #FEF5CA;
			border: none;
		}
		.bouton {
			font-family: "Georgia", serif;
			font-size: 200%;
			background-color: #EEF3E2;
			border: 2px solid black;
		}
		.bouton:hover {
			background-color: #D2691E;
			border: 2px solid darkred;


	</style>
</head>
<body>
	<h1>Températures</h1>
	<table>
		<tr>
		<td>Température actuelle&nbsp;:&nbsp;</td>
		<td>{{temp}}&nbsp;°C</td>
		</tr>
<!--		<tr>
		<td>Température moyenne&nbsp;:&nbsp;</td>
		<td>{{moy}}&nbsp;°C</td>
		</tr> -->
	</table>
	<p>L'objectif de température actuel est de {{obj}}&nbsp;°C.</p>

	<h1>Programmation</h1>
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
		<input class="bouton" value="Programmer la journée" type="submit" />
	</form>
	<div class="footer">Dernière mise à jour : {{heure}}</div>
</body>
</html>
