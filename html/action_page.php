<?php
include 'generic_php.php';

$con = open_database_connection();

// Get the current temperature
if (isset($_POST["get_number_of_agents"]))
{
  $which_user_id = $_POST['which_id'];
	$result = run_select_on_db("SELECT COUNT(*) AS total_agents FROM security_user_current", $con);
	while ($row = mysqli_fetch_array($result))
	{
		$current_location = $row['total_agents'];
	}
  echo $current_location;
}

if (isset($_POST["get_sec_calls"]))
{
  $result = run_select_on_db("SELECT * FROM security_user_calls WHERE call_flag='1'", $con);
  $current_location = "None";
  while ($row = mysqli_fetch_array($result))
	{
    $current_location = $row['lat_data'].",".$row['long_data'].",".$row['id'].",";
  }
  echo $current_location;
}

// Get the current temperature
if (isset($_POST["get_sec_agents_pos"]))
{
	$result = run_select_on_db("SELECT sec_user_id,lat_data,long_data FROM security_user_current", $con);
	while ($row = mysqli_fetch_array($result))
	{
		$current_location .= $row['lat_data'].",".$row['long_data'].",".$row['sec_user_id'].",";
	}
  	echo $current_location;
}

// Get the current temperature
if (isset($_POST["get_all_agents"]))
{
  $result = run_select_on_db("SELECT id,company FROM security_user", $con);
  $current_location = "<select id=\"id_agent_selector\">";
  while ($row = mysqli_fetch_array($result))
  {    
    $current_location .= "<option value=\"".$row['id']."\">".$row['company']."(".$row['id'].")</option>";
  }
  $current_location .= "</select>";
  echo $current_location;
}
?>
