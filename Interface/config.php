<?php
	define('ROOT', 'XXXXX'); //Replace with remote root, eg. https://example.com/thermostat/

	define('DB_HOST', 'XXXXX');
	define('DB_USER', 'XXXXX');
	define('DB_PASSWORD', 'XXXXX');
	define('DB_NAME', 'XXXXX');
	
	define('AUTH_USER', 'XXXXX');
	define('AUTH_PASSWORD', 'XXXXX');
	
	define('COOKIE_NAME', 'XXXXX');
	define('COOKIE_NOONCE', 'XXXXX');
	
	/*********************************************************/
	
	//Returns the mysqli object for a DB connection
	function db_connect() {
		return new mysqli(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
	}
	
	//Returns boolean, true if cookie is valid
	function check_login($db) {
	
		//If the cookie is not set, not logged in
		if(!isset($_COOKIE[COOKIE_NAME])) {
			clear_auth($db);
			return false;
		}
		
		$dbAuth = $db->query("SELECT * FROM `auth` ORDER BY `id` DESC LIMIT 1");
		if($dbAuth->num_rows < 1) {
			clear_auth($db);
			return false;
		}
		
		//Getting auth row from DB
		$row = $dbAuth->fetch_assoc();
		$dbAuth->close();
		
		$salt = $row['salt'];
		$ip = $row['ip'];
		$valid = $row['valid'];
		
		//If invalid in the DB, return false.
		if(!$valid) {
			clear_auth($db);
			return false;
		}
		
		//If IP in DB is different from current IP, return false.
		if($ip !== get_client_ip()) {
			clear_auth($db);
			return false;
		}
		
		$generated_cookie = generate_cookie_value($salt, $ip);
		return $generated_cookie === $_COOKIE[COOKIE_NAME];
	}
	
	function clear_auth($db) {
		//Remove all auth records from DB
		$db->query("DELETE FROM `auth`");
		
		//Remove cookie
		unset($_COOKIE[COOKIE_NAME]);
	}
	
	//Generates the cookie value hash from the salt, expiration and IP address
	function generate_cookie_value($salt, $ip) {
		$s = COOKIE_NOONCE.'_'.AUTH_USER.'_'.AUTH_PASSWORD.'_'.$salt.'_'.$ip;
		return hash('sha512', $s);
	}
	
	function is_https() {
		return (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') || $_SERVER['SERVER_PORT'] == 443;
	}
	
	function generate_random_string($length) {
	    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+{}|:<>?`,.;[]-=';
	    $randomString = '';
	    for ($i = 0; $i < $length; $i++) 
	        $randomString .= $characters[rand(0, strlen($characters) - 1)];
	    return $randomString;
	}
	
	function generate_random_alphanum_string($length) {
	    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
	    $randomString = '';
	    for ($i = 0; $i < $length; $i++) 
	        $randomString .= $characters[rand(0, strlen($characters) - 1)];
	    return $randomString;
	}
	
	function hash_password($password, $salt) {
		return hash('sha512',crypt($password, sprintf('$6$rounds=10000$%s$', $salt)));
	}
	
	function check_password($plaintext, $salt, $hash) {
		return (hash_password($plaintext, $salt) === $hash);
	}
	
	function generate_salt() {
		return generate_random_string(32);
	}
	
	function get_client_ip() {
	    $ipaddress = '';
	    if ($_SERVER['HTTP_CLIENT_IP'])
	        $ipaddress = $_SERVER['HTTP_CLIENT_IP'];
	    else if($_SERVER['HTTP_X_FORWARDED_FOR'])
	        $ipaddress = $_SERVER['HTTP_X_FORWARDED_FOR'];
	    else if($_SERVER['HTTP_X_FORWARDED'])
	        $ipaddress = $_SERVER['HTTP_X_FORWARDED'];
	    else if($_SERVER['HTTP_FORWARDED_FOR'])
	        $ipaddress = $_SERVER['HTTP_FORWARDED_FOR'];
	    else if($_SERVER['HTTP_FORWARDED'])
	        $ipaddress = $_SERVER['HTTP_FORWARDED'];
	    else if($_SERVER['REMOTE_ADDR'])
	        $ipaddress = $_SERVER['REMOTE_ADDR'];
	    else
	        $ipaddress = 'UNKNOWN';
	    return $ipaddress;
	}
	
	function grant_auth($db) {
		$salt = generate_salt();
		$ip = get_client_ip();
		
		clear_auth($db);
		
		//Adding new record
		$insert_sql = sprintf(
			"INSERT INTO `auth` (`salt`, `ip`, `valid`) VALUES ('%s', '%s', 1)",
			$db->real_escape_string($salt),
			$db->real_escape_string($ip)
		);
		if(!$db->query($insert_sql)) {
			printf("Error: %s\n", $db->error);
			return false;
		}
		
		//Set cookie
		set_login_cookie($salt, $ip);
		return true;
	}
	
	function set_login_cookie($salt, $ip) {
		$cookie = generate_cookie_value($salt, $ip);
		setcookie ( COOKIE_NAME, $cookie, 0, '/XXXXX/', 'XXXXX.com', true, true ); //Replace with domain name and directory path
	}
?>