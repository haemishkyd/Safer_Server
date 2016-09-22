<?php
#=======================================================
# Generic Database Access Functions
#=======================================================
#	Run a generic select on the database specified
#-------------------------------------------------------
function run_select_on_db($sql_statement,$sql_connection)
{
	$result=$sql_connection->query($sql_statement);
	if (!$result)
	{
		die('Query Error: ' . mysqli_error());
	}

	return $result;
}
#-------------------------------------------------------
#	General Database Access Logic
#-------------------------------------------------------
function open_database_connection()
{
	#ByteHost
	$con = mysqli_connect("localhost","root","empyrean69","SAfer");
	if (!$con)
	{
		echo "Error: Unable to connect to MySQL." . PHP_EOL;
    echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
    echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
    exit;
	}

	return $con;
}
#-------------------------------------------------------
#	Generate a random password
#-------------------------------------------------------
function randomPassword()
{
    $alphabet = "abcdefghijklmnopqrstuwxyzABCDEFGHIJKLMNOPQRSTUWXYZ0123456789";
    $pass = array(); 						//remember to declare $pass as an array
    $alphaLength = strlen($alphabet) - 1; 	//put the length -1 in cache
    for ($i = 0; $i < 8; $i++) {
        $n = rand(0, $alphaLength);
        $pass[] = $alphabet[$n];
    }
    return implode($pass); 					//turn the array into a string
}
?>
