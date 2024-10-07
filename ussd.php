<?php  
/**  
* USSD application with 3 menus: Welcome, Feelings, and Reasons  
*/

$request = file_get_contents("php://input");
$data = json_decode($request, true);

// Set session ID using SESSION_ID from the request or fall back to a hashed version of MSISDN
$session_id = isset($data['SESSIONID']) ? $data['SESSIONID'] : md5($data['MSISDN']);
session_id($session_id);
session_start();

// Get All Incoming Request Parameters
$ussd_id = $data['USERID'];
$msisdn = $data['MSISDN'];
$user_data = $data['USERDATA'];
$msgtype = $data['MSGTYPE'];
$id = session_id();

// Subsequent dials
if (isset($_SESSION[$id]) && !$msgtype) {  
   // Store user response
   $_SESSION[$id] .= $user_data;  
   $user_dials = preg_split("/\#\*\#/", $_SESSION[$id]);

   // Screen 3: Final response
   if (count($user_dials) == 2) {
       $feeling = $user_dials[0];
       $reason = $user_dials[1];
       $msg = "You are $feeling because of $reason.\nThank you for using my James NOCT1804 USSD Application.";
       $resp = array("USERID" => $ussd_id, "MSISDN" => $msisdn, "USERDATA" => $user_data, "MSG" => $msg, "MSGTYPE" => false);
       echo json_encode($resp);
       session_destroy(); // End the session after the final response
   }
} else {
    // Initial dial
    if (isset($_SESSION[$id]) && $msgtype) {
        session_unset(); // Clear session if the user cancels the initial screen
    }

    // Screen 1: Welcome message
    if (empty($_SESSION[$id])) {
        $_SESSION[$id] = $user_data . "#*#";
        $msg = "Welcome to my James NOCT1804 USSD Application.\nHow are you feeling?\n1. Feeling fine\n2. Feeling frisky\n3. Not well";
        $resp = array("USERID" => $ussd_id, "MSISDN" => $msisdn, "USERDATA" => $user_data, "MSG" => $msg, "MSGTYPE" => true);
        echo json_encode($resp);
    } 
    // Screen 2: Ask for reasons based on feeling
    else {
        $_SESSION[$id] .= $user_data . "#*#"; // Store user response from screen 1
        $feeling = $user_data;

        $msg = "Why are you $feeling?\n1. Money issues\n2. Relationship\n3. A lot";
        $resp = array("USERID" => $ussd_id, "MSISDN" => $msisdn, "USERDATA" => $user_data, "MSG" => $msg, "MSGTYPE" => true);
        echo json_encode($resp);
    }
}

header('Content-type: application/json'); 
?>
