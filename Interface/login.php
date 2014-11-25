<?php
	require_once('config.php');
	
	$db = db_connect();
	$loggedIn = check_login($db);
	
	if($loggedIn === true) {
		$db->close();
		header('Location: '.ROOT);
		exit;
	}
?>
<!DOCTYPE html>
<html>
<head>
	<meta name="viewport" content="width=device-width, user-scalable=no">
	<title>Log in - Thermostat</title>
	<link rel="shortcut icon" href="thermostat.ico">
	<link rel="stylesheet" href="css/reset.css">
	<link rel="stylesheet" href="css/style.css">
</head>
<body>
	<?php if($_REQUEST['error']): ?>
		<div class="panel" id="error">
			<?php echo $_REQUEST['error']; ?>
		</div>
	<?php endif; ?>
	<div class="panel">
		<form method="post" action="actions/login.php">
			<div class="form-field">
				<div class="form-label">
					<label for="username">User:&nbsp;</label>
				</div>
				<div class="form-input">
					<input placeholder="User" type="text" name="username"/>
				</div>
				<div class="clear"></div>
			</div>
			
			<div class="form-field">
				<div class="form-label">
					<label for="username">Password:&nbsp;</label>
				</div>
				<div class="form-input">
					<input placeholder="Password" type="password" name="password"/>
				</div>
				<div class="clear"></div>
			</div>
			
			<input type="hidden" name="error_redir" value="/scoops/login.php" />
			<input type="hidden" name="success_redir" value="/scoops/login.php" />
			
			<div class="form-field">
				<input type="submit" value="Log in"/>
			</div>
		</form>
	</div>
</body>
</html>