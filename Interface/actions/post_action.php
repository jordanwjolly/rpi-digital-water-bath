<?php
	function die_error($redir, $error) {
		$addendum = sprintf(
			'error=%s',
			urlencode($error)
		);
		$redir .= sprintf(
			'%s%s',
			((strpos($redir, '?') === false) ? '?' : '&'),
			$addendum
		);
		
		header('HTTP/1.1 400 Bad Request', true, 400);
		header(sprintf(
			'Location: %s',
			$redir
		));
		exit;
	}
	
	function die_success($redir) {
		header(sprintf(
			'Location: %s',
			$redir
		));
		exit;
	}
	
	/********************************************/
	
	require_once('../config.php');
	
	if(!$_POST) {
		header('HTTP/1.1 400 Bad Request', true, 400);
		exit;
	}
?>