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

	header('Content-type: application/json');
	
	//Validation
	
	if(!is_https())
		die_error('Requests must be made through SSL (https).');
		
	if(!isset($_REQUEST['id']) || trim($_REQUEST['id'])=='')
		die_error('Missing controller ID parameter (id).');
	$id = trim($_REQUEST['id']);
	
	$db = db_connect();
	
	$query = $db->query(sprintf("SELECT * FROM `status` WHERE `id`=%d LIMIT 1", $db->real_escape_string($id)));
	if($query->num_rows < 1) {
		$query->close();
		$db->close();
		die_error('No status found.');
	}
	$status = $query->fetch_assoc();
	$query->close();
	$db->close();
	
	die_success('Success', $status);
?>