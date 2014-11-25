<?php
	require_once('post_action.php');
	
	$errorRedir = ROOT.'login.php';
	$successRedir = ROOT;
	
	if(!isset($_POST['username']) || !$_POST['username'] || count(trim($_POST['username']))<1)
		die_error($errorRedir, 'Missing username.');
	
	if(!isset($_POST['password']) || !$_POST['password'] || count($_POST['password'])<1)
		die_error($errorRedir, 'Missing password.');
		
	$username = strtolower(trim($_POST['username']));
	$password = $_POST['password'];
	
	if($username !== strtolower(AUTH_USER))
		die_error($errorRedir, 'Invalid username or password.');
	
	if($password !== AUTH_PASSWORD)
		die_error($errorRedir, 'Invalid username or password.');
	
	//Username and password correct.
	
	$db = db_connect();
	grant_auth($db);
	$db->close();
	
	die_success($successRedir);

?>