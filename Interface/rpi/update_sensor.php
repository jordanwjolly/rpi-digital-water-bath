<?php
	require_once('../config.php');

	function die_success($message, $data=NULL) {
		$r = array('success'=>true, 'message'=>$message);
		if($data) $r['data'] = $data;
		die(json_encode($r));
	}

	function die_error($error) {
		header("HTTP/1.1 400 Bad Request");
		die(json_encode(array('success'=>false, 'message'=>$error)));
	}
	
	function get_param($key, &$var) {
		global $_POST;
		if(!isset($_POST) || !$_POST) return false;
		if(!isset($_POST[$key]) || !$_POST[$key]) return false;
		$var = $_POST[$key];
		return true;
	}

	header('Content-type: application/json');
	
	//Validation
	
	if(!is_https())
		die_error('Requests must be made through SSL (https).');
	
	if(!isset($_POST) || !$_POST) 
		die_error('Invalid request, must use POST.');
	
	$id = NULL;
	if(!get_param('id', $id)) die_error('Missing id parameter.');
	
	$key = NULL;
	if(!get_param('key', $key)) die_error('Missing key parameter.');
	
	$temperature = NULL;
	if(!get_param('temperature', $temperature)) die_error('Missing temperature parameter.');
	if(!floatval($temperature) || floatval($temperature)<=0) die_error('Invalid temperature parameter.');
	$temperature = floatval($temperature);
	
	$time = NULL;
	if(!get_param('time', $time)) die_error('Missing time parameter.');
	if(!intval($time) || intval($time)<=0) die_error('Invalid time parameter.');
	$time = intval($time);
	
	//Checking ID and key
	
	$db = db_connect();
	
	$query = $db->query(sprintf("SELECT * FROM `sensors` WHERE `id`='%s' LIMIT 1", $db->real_escape_string($id)));
	if($query->num_rows < 1) {
		$query->close();
		$db->close();
		die_error('Invalid sensor ID.');
	}
	$sensor = $query->fetch_assoc();
	$query->close();
	
	$db_hash = $sensor['hash'];
	$db_salt= $sensor['salt'];
	
	if(!check_password($key, $db_salt, $db_hash)) {
		$db->close();
		die_error('Invalid sensor key.');
	}
	
	//Authenticated
	
	$db->query(sprintf(
		"UPDATE `sensors` SET 
		`last_update`=%d, 
		`temperature`=%01.3f
		WHERE `id`='%s' ", 
		$time,
		$temperature,
		$db->real_escape_string($id)
	));
	
	$db->close();
	
	die_success('Sensor values updated successfully.');
?>