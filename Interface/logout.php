<?php
	require_once('config.php');
	$db = db_connect();
	clear_auth($db);
	$db->close();
	
	header('Location: '.ROOT);
?>