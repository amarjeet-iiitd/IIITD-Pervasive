
<?php
	if($_POST["RebootButton"]) {
		echo "<h1>RPi now rebooting</h1>";
		echo "<h2>Try refreshing the page, after some time<br /><hr>";

		system("sudo shutdown -r now");
	}

	if($_POST["sPeriod"]) {
		/*echo $_POST["sPeriod"]."<br/>";
		echo $_POST["pPeriod"]."<br/>";
		echo $_POST["apiKey"]."<br/>";
		echo $_POST["dName"]."<br/>";
		echo $_POST["dLocation"]."<br/>";
		echo $_POST["serverIP"]."<br/>";
		echo $_POST["serverPort"]."<br/>";
		echo $_POST["serverURL"]."<br/>";*/

		$file = fopen("profile", "w");

		if($file == 0) {
			echo "Profile Not Saved"."<br /><hr>";
		}
		else {
			fwrite($file, $_POST["sPeriod"]);
			fwrite($file, "||--||--||");
			fwrite($file, $_POST["pPeriod"]);
			fwrite($file, "||--||--||");
			fwrite($file, $_POST["apiKey"]);
			fwrite($file, "||--||--||");
			fwrite($file, $_POST["dName"]);
			fwrite($file, "||--||--||");
			fwrite($file, $_POST["dLocation"]);
			fwrite($file, "||--||--||");
			fwrite($file, $_POST["serverIP"]);
			fwrite($file, "||--||--||");
			fwrite($file, $_POST["serverPort"]);
			fwrite($file, "||--||--||");
			fwrite($file, $_POST["serverURL"]);

			fclose($file);

			echo "<h1>Profile Saved</h1>"."<br /><hr>";
		}
	}

	//else {
		$file = fopen("profile", "r");

		if($file==0) {
			echo "<h1>DEFAULT VALUES LOADED</h1>"."<br /><hr>";

			$sPeriod = 1;
			$pPeriod = 10;
			$apiKey = "3773bd8cf9594ca7a2a6c0074f73ace7";
			$dName = "RPi-RJ";
			$dLocation = "RJ-Home";
			$serverIP = "sensoract.iiitd.edu.in";
			$serverPort = 9000;
			$serverURL = "/upload/wavesegment";
		}
		else {
			$line = fgets($file);

			$data = explode("||--||--||", $line);

			$sPeriod = $data[0];
			$pPeriod = $data[1];
			$apiKey = $data[2];
			$dName = $data[3];
			$dLocation = $data[4];
			$serverIP = $data[5];
			$serverPort = $data[6];
			$serverURL = $data[7];

			fclose($file);
		}
	//}
?>

<html>
	<body>
		<h1>RPi Configuration Page</h1>

		<form action="/" method="post">
			<p>Sampling Period (sec): <input id="id_sPeriod" name="sPeriod" type="text" value="<?php echo $sPeriod ?>" /></p>
			<p>Publish Period (sec): <input id="id_pPeriod" name="pPeriod" type="text" value="<?php echo $pPeriod ?>" /></p>
			<p>API Key: <input id="id_apiKey" name="apiKey" type="text" value="<?php echo $apiKey ?>" /></p>
			<p>Device Name: <input id="id_dName" name="dName" type="text" value="<?php echo $dName ?>" /></p>
			<p>Device Location: <input id="id_dLocation" name="dLocation" type="text" value="<?php echo $dLocation ?>" /></p>
			<p>Server IP: <input id="id_serverIP" name="serverIP" type="text" value="<?php echo $serverIP ?>" /></p>
			<p>Server Port: <input id="id_serverPort" name="serverPort" type="text" value="<?php echo $serverPort ?>" /></p>
			<p>Server URL: <input id="id_serverUrl" name="serverURL" type="text" value="<?php echo $serverURL ?>" /></p>

			<input type="submit" value="Submit" />
		</form>

		<form action="/" method="post">
			<input type="submit" name="RebootButton" value="Reboot" />
		</form>
	</body>
</html>
