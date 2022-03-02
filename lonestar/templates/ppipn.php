<?php
define("DEBUG", 1);
define("USE_SANDBOX", 0);
define("LOG_FILE", "./ipn.log");
if (DEBUG == true) error_log(date('[Y-m-d H:i e] '). "Starting IPN" . PHP_EOL, 3, LOG_FILE);

require_once("core.php");
if (DEBUG == true) error_log("core.php loaded" . PHP_EOL, 3, LOG_FILE);
require_once("dbapi.php");
if (DEBUG == true) error_log("dbapi.php loaded" . PHP_EOL, 3, LOG_FILE);
require_once("confemail.php");
if (DEBUG == true) error_log("confemail.php loaded" . PHP_EOL, 3, LOG_FILE);

$raw_post_data = file_get_contents('php://input');
$raw_post_array = explode('&', $raw_post_data);
$myPost = array();
foreach ($raw_post_array as $keyval) {
	$keyval = explode ('=', $keyval);
	if (count($keyval) == 2)
		$myPost[$keyval[0]] = urldecode($keyval[1]);
}
// read the post from PayPal system and add 'cmd'
$req = 'cmd=_notify-validate';
if(function_exists('get_magic_quotes_gpc')) {
	$get_magic_quotes_exists = true;
}
foreach ($myPost as $key => $value) {
	if($get_magic_quotes_exists == true && get_magic_quotes_gpc() == 1) {
		$value = urlencode(stripslashes($value));
	} else {
		$value = urlencode($value);
	}
	$req .= "&$key=$value";
}
if (DEBUG == true) error_log("Finished reading post data." . PHP_EOL, 3, LOG_FILE);
// Post IPN data back to PayPal to validate the IPN data is genuine
// Without this step anyone can fake IPN data
if(USE_SANDBOX == true) {
	$paypal_url = "https://www.sandbox.paypal.com/cgi-bin/webscr";
} else {
	$paypal_url = "https://www.paypal.com/cgi-bin/webscr";
}
$ch = curl_init($paypal_url);
if ($ch == FALSE) {
	return FALSE;
}
curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_RETURNTRANSFER,1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $req);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 1);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2);
curl_setopt($ch, CURLOPT_FORBID_REUSE, 1);
if (DEBUG == true) {
	curl_setopt($ch, CURLOPT_HEADER, 1);
	curl_setopt($ch, CURLINFO_HEADER_OUT, 1);
}

curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 30);
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Connection: Close'));
// CONFIG: Please download 'cacert.pem' from "http://curl.haxx.se/docs/caextract.html" and set the directory path
// of the certificate as shown below. Ensure the file is readable by the webserver.
// This is mandatory for some environments.
$cert = __DIR__ . "/cacert.pem";
curl_setopt($ch, CURLOPT_CAINFO, $cert);

if (DEBUG == true) error_log("curl options all set." . PHP_EOL, 3, LOG_FILE);
$res = curl_exec($ch);
if (curl_errno($ch) != 0) // cURL error
	{
	if(DEBUG == true) {	
		error_log(date('[Y-m-d H:i e] '). "Can't connect to PayPal to validate IPN message: " . curl_error($ch) . PHP_EOL, 3, LOG_FILE);
	}
	curl_close($ch);
	exit;
} else {
		// Log the entire HTTP response if debug is switched on.
		if(DEBUG == true) {
			error_log(date('[Y-m-d H:i e] '). "HTTP request of validation request:". curl_getinfo($ch, CURLINFO_HEADER_OUT) ." for IPN payload: $req" . PHP_EOL, 3, LOG_FILE);
			error_log(date('[Y-m-d H:i e] '). "HTTP response of validation request: $res" . PHP_EOL, 3, LOG_FILE);
		}
		curl_close($ch);
}
// Inspect IPN validation result and act accordingly
// Split response headers and payload, a better way for strcmp
$tokens = explode("\r\n\r\n", trim($res));
$res = trim(end($tokens));
if (strcmp($res, "VERIFIED") == 0) {
	$item_name = $_POST['item_name'];
	$payment_status = $_POST['payment_status'];
	$payment_amount = $_POST['mc_gross'];
	$payment_currency = $_POST['mc_currency'];
	$payer_email = $_POST['payer_email'];
	$receiver_email = $_POST['receiver_email'];
	$runnerid = $_POST['invoice'];
	$temp = explode(",", $_POST['custom']);
	$teamid = $temp[0];
	$teampay = $temp[1];
	$newteam = $temp[2];
	$orderid = $temp[3];

	if(DEBUG == true) {
		error_log("team id: " . $teamid . PHP_EOL, 3, LOG_FILE);
		error_log("runner id: " . $runnerid . PHP_EOL, 3, LOG_FILE);
		error_log("team pay: " . $teampay . PHP_EOL, 3, LOG_FILE);
		error_log("new team: " . $newteam . PHP_EOL, 3, LOG_FILE);
		error_log("order id: " . $orderid . PHP_EOL, 3, LOG_FILE);
	}

	// check whether the payment_status is Completed
	if ($payment_status != "Completed") {
		error_log("Payment not completed: " . $payment_status . PHP_EOL, 3, LOG_FILE);
		exit;
	}

	// check that receiver_email is your PayPal email
	if ($receiver_email != "admin@TexasIndependenceRelay.com") {
		error_log("Payment not made to TIR account; it was made to: " . $receiver_email . " (".$runnerid.")" . PHP_EOL, 3, LOG_FILE);
		exit;
	}

	// process payment and mark item as paid.
	$conn = mysql_conn();

	$tsql = "";
	if ($teampay == "1" && $newteam == "1") $tsql = "Update `Team` Set IsPaid=1, PaidAmount=? Where ID = ?";
	else $tsql = "Update Runner Set IsPaid=1, PaidAmount=? Where ID = ?";
	$tags = array();
	$stmt = mysqli_prepare($conn, $tsql);
	if ($stmt == FALSE) {
	} else {
		if ($teampay == "1" && $newteam == "1") $stmt->bind_param("di", $payment_amount, $teamid);
		else $stmt->bind_param("di", $payment_amount, $runnerid);
		$stmt->execute();
		mysqli_stmt_close($stmt);
	}

	//orders are marked as paid but no amount is marked since the amount was rolled into the registration fee
	if ($orderid != null && $orderid != "") {
		$tsql = "Update `Order` Set IsPaid=1 Where ID=?;";
		try {
			$stmt = mysqli_prepare($conn, $tsql);
			$stmt->bind_param("i", $orderid);
			$stmt->execute();
			mysqli_stmt_close($stmt);
		} catch (Exception $ex) {
			error_log("SQL Error marking order as paid: " . $ex->getMessage().PHP_EOL,3,LOG_FILE);
		}
	}


	if ($newteam == "1") {
		$joincode = findNewJoinCode($conn);
		if (DEBUG == true) {
			error_log("Join code: " . $joincode . PHP_EOL, 3, LOG_FILE);
		}
		$tsql = "Update `Team` Set JoinCode=?, Bib=(ID-1000) Where ID=?";
		$stmt = mysqli_prepare($conn, $tsql);
		if ($stmt == FALSE) {
		} else {
			$stmt->bind_param("ii", $joincode, $teamid);
			$stmt->execute();
			mysqli_stmt_close($stmt);
		}
	}

	// send email
	$emailret = sendConfirmationEmail($teamid, $runnerid);
	if ($emailret !== true && DEBUG == true) {
		error_log(date('[Y-m-d H:i e] '). "Email failed to send: $emailret ". PHP_EOL, 3, LOG_FILE);		
	}
	
	mysqli_close($conn);
	
	if(DEBUG == true) {
		error_log(date('[Y-m-d H:i e] '). "Verified IPN: $req ". PHP_EOL, 3, LOG_FILE);
	}
} else if (strcmp ($res, "INVALID") == 0) {
	// log for manual investigation
	// Add business logic here which deals with invalid IPN messages
	if(DEBUG == true) {
		error_log(date('[Y-m-d H:i e] '). "Invalid IPN: $req" . PHP_EOL, 3, LOG_FILE);
		error_log(date('[Y-m-d H:i e] '). "Raw post data: $raw_post_data" . PHP_EOL, 3, LOG_FILE);
	}
}
?>