<?php
	require_once('config.php');
	
	$db = db_connect();
	$loggedIn = check_login($db);
	
	if(!$loggedIn) {
		$db->close();
		header('Location: login.php');
		exit;
	}
	
	define('CONTROLLER_ID', 1);
	define('UPDATE_MS', 200);
	define('WARNING_TIME_SEC', 250);
?>
<!DOCTYPE html>
<html>
<head>
	<meta name="viewport" content="width=device-width, user-scalable=no">
	<title>Thermostat</title>
	<link rel="shortcut icon" href="thermostat.ico">
	<link rel="stylesheet" type="text/css" href="fonts/symbolset/ss-geomicons-squared.css">
	<link rel="stylesheet" href="css/reset.css">
	<link rel="stylesheet" href="css/style.css">
</head>
<body role="main" >
	<div id="canvas">
		<div class="panel">
			<div id="warning-panel">
				<div class="ss-alert icons float-l"></div>
				<div id="warning-text">Sensors are unresponsive, please check connections.</div>
				<div class="clear"></div>
			</div>
			<div id="current-temp"></div>
			
			<div id="set-range">
				<div id="range-low" class="set-range-side">
					<div class="up-down-buttons">
						<div class="up-button button disabled"></div>
						<div class="down-button button disabled"></div>
					</div>
					<div class="range-temp"></div>
					<div class="clear"></div>
				</div>				
				<div id="range-high" class="set-range-side">
					<div class="range-temp"></div>
					<div class="up-down-buttons">
						<div class="up-button button disabled"></div>
						<div class="down-button button disabled"></div>
					</div>
					<div class="clear"></div>
				</div>
				<div class="clear"></div>
			</div>
			
			<div id="mode-buttons">
				<div class="left-col" id="compressor-mode-buttons">
					<h1>Compressor</h1><br/>
					<div id="button-compressor-auto" class="button disabled full-width-button">Auto</div>
					<div id="button-compressor-cool" class="button disabled full-width-button">Cooling</div>
					<div id="button-compressor-heat" class="button disabled full-width-button">Heating</div>
					<div id="button-compressor-off" class="button disabled full-width-button">Off</div>
				</div>
				<div class="right-col" id="fan-mode-buttons">
					<h1>Fan</h1><br/>
					<div id="button-fan-auto" class="button disabled full-width-button">Auto</div>
					<div id="button-fan-on" class="button disabled full-width-button">On</div>
				</div>
				<div class="clear"></div>
			</div>
		</div>
	</div>
	
	<script>
		var hasLoadedSettings = false;
		var hasLoadedStatus = false;
		var isUpdatingSettings = false;
		var currentError = null;
		
		var setMin = 0;
		var setMax = 0;
	</script>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
	<script>
		function main() {
			getSettings();
			getStatus();
			setButtonClickHandlers();
		}
		
		function setButtonClickHandlers() {
			jQuery('#range-low .down-button').click(function() {
				if(setMin != 0 && !jQuery(this).hasClass('disabled'))
					updateSetting('temperature_min', (setMin-1));
			});
			jQuery('#range-low .up-button').click(function() {
				if(setMin != 0 && !jQuery(this).hasClass('disabled'))
					updateSetting('temperature_min', (setMin+1));
			});
			
			jQuery('#range-high .down-button').click(function() {
				if(setMax != 0 && !jQuery(this).hasClass('disabled'))
					updateSetting('temperature_max', (setMax-1));
			});
			jQuery('#range-high .up-button').click(function() {
				if(setMax != 0 && !jQuery(this).hasClass('disabled'))
					updateSetting('temperature_max', (setMax+1));
			});
			
			jQuery('#button-compressor-off').click(function() {
				if(!jQuery(this).hasClass('disabled'))
					updateSetting('compressor_mode', 'off');
			});
			
			jQuery('#button-compressor-heat').click(function() {
				if(!jQuery(this).hasClass('disabled'))
					updateSetting('compressor_mode', 'heat');
			});
			
			jQuery('#button-compressor-cool').click(function() {
				if(!jQuery(this).hasClass('disabled'))
					updateSetting('compressor_mode', 'cool');
			});
			
			jQuery('#button-compressor-auto').click(function() {
				if(!jQuery(this).hasClass('disabled'))
					updateSetting('compressor_mode', 'auto');
			});
			
			jQuery('#button-fan-auto').click(function() {
				if(!jQuery(this).hasClass('disabled'))
					updateSetting('fan_mode', 'auto');
			});
			
			jQuery('#button-fan-on').click(function() {
				if(!jQuery(this).hasClass('disabled'))
					updateSetting('fan_mode', 'on');
			});
		}
		
		function updateSetting(field, value) {
			if(isUpdatingSettings) return;
			isUpdatingSettings = true;
			
			jQuery.post(
				'actions/update_setting.php', 
				{id:1, field:field, value:value}, 
				function(data) { 
					isUpdatingSettings = false;
					console.log(data); 
				}
			);
		}
		
		function getStatus() {
			jQuery.getJSON('rpi/get_status.php?id=<?php echo CONTROLLER_ID; ?>', function(data) {
				statusRefreshed(data.data, !hasLoadedStatus);
				hasLoadedStatus = true;
			});
		}
		
		function getSettings() {
			jQuery.getJSON('rpi/get_settings.php?id=<?php echo CONTROLLER_ID; ?>', function(data) {
				settingsRefreshed(data.data, !hasLoadedSettings);
				hasLoadedSettings=true;
			});
		}
		
		function statusRefreshed(status, firstTime) {
			setBodyClass(status);
			checkResponsiveTime(parseInt(status.last_update));
			
			setTimeout(getStatus, <?php echo UPDATE_MS; ?>);
		}
		
		function checkResponsiveTime(lastUpdateTime) {
			var time = Math.round(new Date().getTime() / 1000);
			var errorCode = 'old_status';
			if(currentError === null && (lastUpdateTime + <?php echo WARNING_TIME_SEC; ?>) < time) {
				currentError = errorCode;
				showWarning('Status has not been updated, controller may be offline.');
			}
			else if(currentError == errorCode && !((lastUpdateTime + <?php echo WARNING_TIME_SEC; ?>) < time)) {
				currentError = null;
				hideWarning();
			}
		}
		
		function showWarning(message) {
			jQuery('#canvas').removeClass('heating');
			jQuery('#canvas').removeClass('fan');
			jQuery('#canvas').removeClass('off');
			jQuery('#canvas').removeClass('cooling');
			jQuery('#canvas').addClass('warning');
			
			jQuery('#warning-text').text(message);
			jQuery('#warning-panel').show();
		}
		
		function hideWarning() {
			jQuery('#warning-panel').hide();
		}
		
		function setBodyClass(status) {
			if(currentError!==null) return;
			
			if(status.cooling == '1') {
				jQuery('#canvas').removeClass('heating');
				jQuery('#canvas').removeClass('fan');
				jQuery('#canvas').removeClass('off');
				jQuery('#canvas').addClass('cooling');
			}
			else if(status.heating == '1') {
				jQuery('#canvas').removeClass('cooling');
				jQuery('#canvas').removeClass('fan');
				jQuery('#canvas').removeClass('off');
				jQuery('#canvas').addClass('heating');
			}
			else if(status.fan == '1') {
				jQuery('#canvas').removeClass('cooling');
				jQuery('#canvas').removeClass('heating');
				jQuery('#canvas').removeClass('off');
				jQuery('#canvas').addClass('fan');
			}
			else {
				jQuery('#canvas').removeClass('cooling');
				jQuery('#canvas').removeClass('heating');
				jQuery('#canvas').removeClass('fan');
				jQuery('#canvas').addClass('off');
			}
		}
		
		function settingsRefreshed(settings, firstTime) {
			updateCurrentTemp(settings.observed_temperature);
			updateSetTempRange(settings.temperature_min, settings.temperature_max);
			updateCompressorButtons(settings.compressor_mode);
			updateFanButtons(settings.fan_mode);
			checkSettingsValid(settings.valid);
			
			setTimeout(getSettings, <?php echo UPDATE_MS; ?>);
		}
		
		function checkSettingsValid(valid) {
			var errorCode = 'invalid_settings';
			if(currentError === null && !valid) {
				currentError = errorCode;
				showWarning('Settings invalid, please check sensors.');
			}
			else if(currentError == errorCode && valid) {
				currentError = null;
				hideWarning();
			}
		}
		
		function updateCompressorButtons(mode) {
			jQuery('#compressor-mode-buttons .button').removeClass('disabled');
			jQuery('#button-compressor-'+mode).addClass('disabled');
		}
		
		function updateFanButtons(mode) {
			jQuery('#fan-mode-buttons .button').removeClass('disabled');
			jQuery('#button-fan-'+mode).addClass('disabled');		
		}
		
		function updateCurrentTemp(temp) {
			temp = temp.toFixed(2);
			var full = temp.substr(0, 2);
			var dec = temp.substr(2, temp.length-2);
			jQuery('#current-temp').html('<span -large>'+full+'</span><span -small>'+dec+' &deg;F</span>');
		}
		
		function updateSetTempRange(min, max) {
			setMin = min;
			setMax = max;
			
			jQuery('#range-low .range-temp').text(min);
			jQuery('#range-high .range-temp').text(max);
			
			jQuery('#range-low .button, #range-high .button').removeClass('disabled');
			if(max-min <= 2) {
				jQuery('#range-low .up-button').addClass('disabled');
				jQuery('#range-high .down-button').addClass('disabled');
			} else {
				jQuery('#range-low .up-button').removeClass('disabled');
				jQuery('#range-high .down-button').removeClass('disabled');
			}
		}
		
		jQuery(document).ready(main);
	</script>
</body>
</html>
<?php $db->close(); ?>