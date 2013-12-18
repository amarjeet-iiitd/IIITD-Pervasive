var refreshTime = "";

var myEvent;

$(document).ready(function(){
	$("#RefreshTimeSet").click(updateRefreshTime);

	refresh();
	
	$("#Mode-2").click(function() {
		$("#Mode-1-Parameters").hide();
		$("#Mode-2-Parameters").show();
	});

	$("#Mode-1").click(function() {
		$("#Mode-2-Parameters").hide();
		$("#Mode-1-Parameters").show();
	});


	loadProfile();

	$("#SaveDeviceParameters").click(function() {
		saveDevice();
	});

	$("#SaveSensoractParameters").click(function() {
		saveSensoract();
	});
	
	$("#SaveConnectionParameters").click(function() {
		saveConnection();
	});
	
	$("#SaveLogParameters").click(function() {
		saveLog();
	});
	
	$("#Reboot").click(function() {
		console.log("Trying to Reboot");
		xhr = $.ajax({
			url: "reboot.php"
		});

		xhr.done(function(msg) {
			console.log(msg);
			alert("Rebooting Device\nPlease Refresh after some time");
		});
	});
});

function updateRefreshTime() {
	console.log("New Refresh Time : " + $('#RefreshTime').val());
	refreshTime = $('#RefreshTime').val();
}

/**
 * Saving Device Parameters
 **/
function saveDevice() {
	
	mode = 1;
	if($("#Mode-2").prop("checked"))
		mode = 2;

	xhr = $.ajax({
		type: "POST",
		url: "save_values.php",
		data: {Type:"device",
				Values: mode
					+ " " + $("#SamplingPeriod").val()
					+ " " + $("#PublishPeriod").val()
					+ " " + $("#StoreLength").val()
					+ " " + $("#StorePath").val()
					+ " " + $("#UploadPeriod").val()}
	});
	
	xhr.done(function(msg) {
		console.log(msg);
		
		if(msg === "SUCCESS\n")
			alert("Saved Device Parameters");
		else
			alert("Error Saving Device Parameters");
	});
}

/**
 * Saving Sensoract Parameters
 **/
function saveSensoract() {
	
	xhr = $.ajax({
		type: "POST",
		url: "save_values.php",
		data: {Type:"sensoract",
				Values: $("#APIkey").val()
					+ " " + $("#DeviceName").val()
					+ " " + $("#DeviceLocation").val()}
	});
	
	xhr.done(function(msg) {
		console.log(msg);
		
		if(msg === "SUCCESS\n")
			alert("Saved Sensoract Parameters");
		else
			alert("Error Saving Sensoract Parameters");
	});
}

/**
 * Saving Connection Parameters
 **/
function saveConnection() {
	
	xhr = $.ajax({
		type: "POST",
		url: "save_values.php",
		data: {Type:"connection",
				Values: $("#ServerIP").val()
					+ " " + $("#ServerPort").val()
					+ " " + $("#ServerURL").val()}
	});
	
	xhr.done(function(msg) {
		console.log(msg);
		
		if(msg === "SUCCESS\n")
			alert("Saved Connection Parameters");
		else
			alert("Error Saving Connection Parameters");
	});
}

/**
 * Saving Log Parameters
 **/
function saveLog() {
	
	enableLog = "True";
	
	if($("#EnableLog").prop("checked") === false)
		enableLog = "False";
	
	logTags = $("#LogTags").val();
	
	if(logTags === null)
		logTags = "";
	
	console.log("LogTags Saving - " + "('" + logTags.toString().replace(/,/g, "','") + "')");
	
	xhr = $.ajax({
		type: "POST",
		url: "save_values.php",
		data: {Type:"log",
				Values: enableLog
					+ " " + $("#LogDir").val()
					+ " " + logTags.toString().replace(/,/g, "','")}
	});
	
	xhr.done(function(msg) {
		console.log(msg);
		
		if(msg === "SUCCESS\n")
			alert("Saved Log Parameters");
		else
			alert("Error Saving Log Parameters");
	});
}

/**
* Loading Profile Values
**/
function loadProfile() {

	xhr = $.ajax({
		url: "load_values.php"
	})

	xhr.done(function(msg){
		lines = msg.split('\n');
//		console.log(lines);

		if(lines[0]==='SUCCESS') {
			console.log('Loading Values Successful');
		}
		else{
			console.log(msg);
			return;
		}

		for(i=1 ; i<lines.length-1 ; i++) {
			property = lines[i].split(" ")[0];
			value = lines[i].split(" ")[1];

			console.log(lines[i]);

			if(property === "Mode") {
				if(value === "1")
					$("#Mode-1").click();
				else
					$("#Mode-2").click();
			}

			else if(property === "EnableLog")
				$("#EnableLog").prop("checked", value.toLowerCase());
			
			else if(property === "LogTags") {
				tags = lines[i].replace("LogTags (", "").replace(")", "").replace(/'/g, "").split(", ");
				
				if(tags.length === 1) {
					tags[0] = tags[0].replace(/,/g, "");
				}
				$("#" + property).val(tags);
			}
			else {
				$("#" + property).val(value);
			}
		}
	});
}

/**
 * Refresh Sensor Values on Webpage (REPEATS ITSELF)
 **/
function refresh() {
	
	if(refreshTime === "") {
		$('#RefreshTime').val(2);
		refreshTime = 2;
	}

	setTimeout(refresh, parseFloat(refreshTime)*1000);
	//console.log('refresh values');
	
	xhr = $.ajax({
			url: "sensor_values.php"
		});

	xhr.done(function(msg) {
			$('#TEMP_VAL').text(msg.split("\n")[0]);
			$('#LIGHT_VAL').text(msg.split("\n")[1]);
			$('#PIR_VAL').text(msg.split("\n")[2]);
		});
}
