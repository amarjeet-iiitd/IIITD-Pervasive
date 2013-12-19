<?php
	include("config.php");
	//system("python ".$PATH."/profile_io/server_load.py");
	
	//print_r($_POST);
	
	$type = $_POST["Type"];
	$values = $_POST["Values"];
	
	$str = "sudo python"." ".$PATH."/server_save.py"." ".$type." ".$values;
	
	//~ echo $str;
	system($str);
?>
