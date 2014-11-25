<?php
	require_once('../config.php');
	
	define('IN_THE_BLIND_TIME', 300);
	
	function die_success($message, $data=NULL) {
		$r = array('success'=>true, 'message'=>$message);
		if($data) $r['data'] = $data;
		die(json_encode($r));
	}

	function die_error($error) {
		header("HTTP/1.1 400 Bad Request");
		die(json_encode(array('success'=>false, 'message'=>$error)));
	}

	header('Content-type: application/json');
	
	//Validation
	
	if(!is_https())
		die_error('Requests must be made through SSL (https).');
	
	$result = array();
	
	$db = db_connect();
	
	$query = $db->query("SELECT * FROM `settings` ORDER BY `id` DESC LIMIT 1");
	if($query->num_rows < 1) {
		$query->close();
		$db->close();
		die_error('No settings found.');
	}
	$settings = $query->fetch_assoc();
	$query->close();
	
	$result['fan_mode'] = $settings['fan_mode'];
	$result['compressor_mode'] = $settings['compressor_mode'];
	$result['temperature_min'] = intval($settings['temperature_min']);
	$result['temperature_max'] = intval($settings['temperature_max']);
	$result['temperature_threshold'] = floatval($settings['temperature_threshold']);
	
	$temp = 0;
	$invalid = false;
	// Null sensor, calculate average
	if($settings['observed_sensor']==NULL) {
		$query = $db->query("SELECT * FROM `sensors` WHERE `enabled`=1");
		if($query->num_rows < 1) {
			$query->close();
			$db->close();
			die_error('No sensors found.');
		}
		
		$temp = 0;
		$count = 0;
		while($sensor = $query->fetch_assoc()) {
			$lastUpdate = $sensor['last_update'];
			if($lastUpdate+IN_THE_BLIND_TIME < time())
				continue;
			
			$temp += floatval($sensor['temperature']);
			$count++;
		}
		$query->close();
		
		if($count>0)
			$result['observed_temperature'] = $temp/$count;
		else {
			$result['observed_temperature'] = 0;
			$invalid = true;
		}
	}
	
	// Use specific sensor as observation
	else {
		$query = $db->query(sprintf("SELECT * FROM `sensors` WHERE `id`='%s'", $settings['observed_sensor']));
		if($query->num_rows < 1) {
			$query->close();
			$db->close();
			die_error('No sensors found.');
		}
		$sensor = $query->fetch_assoc();
		$query->close();
		$result['observed_temperature'] = floatval($sensor['temperature']);
		
		$lastUpdate = $sensor['last_update'];
		if($lastUpdate+IN_THE_BLIND_TIME < time())
			$invalid = true;
	}
	
	$result['valid'] = !$invalid;
	
	$db->close();
	
	die_success('Success', $result);
?>