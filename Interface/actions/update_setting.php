<?php
	require_once('post_action.php');
	require_once('../config.php');
	
	$errorRedir = ROOT;
	$successRedir = ROOT;
	
	$db = db_connect();
	$loggedIn = check_login($db);
	
	if(!$loggedIn) {
		$db->close();
		header('Location: login.php');
		exit;
	}
	
	//Authenticated, so now check params

	if(!isset($_POST['id']) || !$_POST['id'] || count(trim($_POST['id']))<1)
		die_error($errorRedir, 'Missing controller ID.');
	$id = trim($_POST['id']);
	
	if(!isset($_POST['field']) || !$_POST['field'] || count($_POST['field'])<1)
		die_error($errorRedir, 'Missing settings field.');
	$field = trim($_POST['field']);
	
	if(!isset($_POST['value']) || count($_POST['value'])<1)
		die_error($errorRedir, 'Missing settings value.');
	$value = trim($_POST['value']);
	
	//Params looks good, so lets attempt the update in one go because fuck it 
	$update_sql = sprintf(
		"UPDATE `settings` SET `%s` = '%s' WHERE `id` = %d ",
		$db->real_escape_string($field),
		$db->real_escape_string($value),
		$db->real_escape_string($id)
	);
	if(!$db->query($update_sql)) {
		$error = $db->error;
		$db->close();
		echo(sprintf('Error updating field: %s', $error));
	}
	
	die_success($successRedir);
?>