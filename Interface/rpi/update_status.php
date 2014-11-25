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
	
	$data = NULL;
	if(!get_param('data', $data)) die_error('Missing data parameter.');
	if(trim($data)=='')
		die_error('Invalid data parameter.');
	if(!json_decode($data))
		die_error('Invalid data parameter.');
	$data = json_decode($data);
	if(!$data)
		die_error('Invalid data parameter.');
		
	$db = db_connect();
	
	//First check and make sure this is a valid controller
	$dbController = $db->query( sprintf(
		"SELECT * FROM `controllers` WHERE `id`='%s' ",
		$db->real_escape_string($id)
	));
	if($dbController->num_rows < 1) {
		$dbController->close();
		$db->close();
		die_error('Invalid controller.');
	}
	
	$controllerRow = $dbController->fetch_assoc();
	$dbController->close();
	
	//Now see if it's authorized
	$dbSalt = $controllerRow['salt'];
	$genHash = hash_password($key, $dbSalt);
	
	if($genHash != $controllerRow['hash']) {
		$db->close();
		die_error('Unauthorized controller.');
	}
	
	//Controller is valid and authorized
	//Now do actual update
	
	$update_sql = sprintf(
		"UPDATE `status` SET `last_update` = %d, `last_fan_disable_time` = %d, `last_compressor_enable_time` = %d, `last_compressor_disable_time` = %d, `last_settings_update_time` = %d, `fan` = %d, `cooling` = %d, `heating` = %d WHERE `controller` = '%s' ",
		time(),
		$data->lastFanDisableTime,
		$data->lastCompressorEnableTime,
		$data->lastCompressorDisableTime,
		$data->lastSettingsUpdateTime,
		($data->fan === true ? 1 : 0),
		($data->cooling === true ? 1 : 0),
		($data->heating === true ? 1 : 0),
		$db->real_escape_string($id)
	);
	
	if(!$db->query($update_sql)) {
		$error = $db->error;
		$db->close();
		die_error(sprintf('Error updating status: %s', $error));
	}
	
	$db->close();
	die_success('Status update successful.');
?>