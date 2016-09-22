<!DOCTYPE html>
<?php
include 'generic_php.php';
?>
<html>
  <head>
    <title>Simple Map</title>
    <meta name="viewport" content="initial-scale=1.0">
    <meta charset="utf-8">
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 70%;
      }
      #header {
        height: 30%;
      }
    </style>
    <script src="js/jquery-2.1.4.min.js"></script>
    <script>
      var number_of_available_agents;
      var map;
      var lat_var_data=-27.118622;
      var long_var_data=30.00092;
      var image;
      var marker=[];
      var marker_lat_array = [];
      var marker_lon_array = [];
      var marker_id_array = [];

      function initMap() {
        image = {
          url: 'shield.png',
          // This marker is 20 pixels wide by 32 pixels high.
          size: new google.maps.Size(50, 51),
          // The origin for this image is (0, 0).
          origin: new google.maps.Point(0, 0),
          // The anchor for this image is the base of the flagpole at (0, 32).
          anchor: new google.maps.Point(25, 25)
        };

        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: parseFloat(lat_var_data), lng: parseFloat(long_var_data)},
          zoom: 16
        });
      }

      function regular_functions()
      {
        get_reg_graph_data = $.ajax(
  			{
  				url		: "action_page.php",
  				type : "POST",
  				data :
  				{
  					get_sec_agents_pos : "0"
  				}
  			});

  			get_reg_graph_data.done(function(response, textStatus, jqXHR)
  			{
          var array_idx = 0;
          var array = response.split(',');

          for (idx=0;idx<parseInt(number_of_available_agents);idx++)
          {
            marker_lat_array[idx] = array[array_idx++];
            marker_lon_array[idx] = array[array_idx++];
            marker_id_array[idx] = array[array_idx++];
            marker[idx].setPosition( new google.maps.LatLng( parseFloat(marker_lat_array[idx]), parseFloat(marker_lon_array[idx])) );
            //map.panTo( new google.maps.LatLng(parseFloat(marker_lat_array[idx]), parseFloat(marker_lon_array[idx])));
          }
        });

        get_called_agents = $.ajax(
  			{
  				url		: "action_page.php",
  				type : "POST",
  				data :
  				{
  					get_sec_calls : "0"
  				}
  			});

        get_called_agents.done(function(response, textStatus, jqXHR)
  			{
          var array_idx = 0;
          var array = response.split(',');
          if (response == "None")
          {
            $("#id_called_agents").html("No Calls");
          }
          else {
              $("#id_called_agents").html("Agent "+array[2]+" has been called to lat:"+array[0]+",long:"+array[1]);
          }

        });
      }

      window.setInterval(function()
    	{
    		regular_functions();
    	}, 5000);

      $(document).ready(function()
    	{
        get_all_agents = $.ajax(
        {
          url   : "action_page.php",
          type : "POST",
          data :
          {
            get_all_agents : "0"
          }
        });

        get_all_agents.done(function(response, textStatus, jqXHR)
        {
          $("#id_list_all_agents").html(response);
        });


        get_graph_data = $.ajax(
  			{
  				url		: "action_page.php",
  				type : "POST",
  				data :
  				{
  					get_sec_agents_pos : "0"
  				}
  			});

  			get_graph_data.done(function(response, textStatus, jqXHR)
  			{
          var array = response.split(',');
          for (idx=0;idx<parseInt(number_of_available_agents);idx++)
          {
            marker_lat_array[idx] = array[array_idx++];
            marker_lon_array[idx] = array[array_idx++];
            marker_id_array[idx] = array[array_idx++];
          }
        });

        get_number_of_agents = $.ajax(
  			{
  				url		: "action_page.php",
  				type : "POST",
  				data :
  				{
  					get_number_of_agents : "0"
  				}
  			});

        get_number_of_agents.done(function(response, textStatus, jqXHR)
        {
          $("#id_num_agents").html(response+" Agents Available");
          number_of_available_agents = response;

          for (idx=0;idx<parseInt(number_of_available_agents);idx++)
          {
            marker[idx] = new google.maps.Marker({
              position: {lat: parseFloat(marker_lat_array[idx]),lng: parseFloat(marker_lon_array[idx])},
              map:      map,
              icon:     image
            });
          }
        });

        $(document).on('change',"#id_agent_selector",function(){
          var selected_agent_array_idx;

          for (idx=0;idx<parseInt(number_of_available_agents);idx++)
          {
            if ($("#id_agent_selector").val() ==  marker_id_array[idx])
            {
              selected_agent_array_idx = idx;
            }
          }
          map.panTo( new google.maps.LatLng(parseFloat(marker_lat_array[selected_agent_array_idx]), 
                                            parseFloat(marker_lon_array[selected_agent_array_idx])));
        });

      });
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBheJpPIla7vSIRVNQMkMCjNFb5hhW8RL0&callback=initMap">
    </script>
  </head>
  <body>
    <div><h1 style="text-align: center">SAfer</h1></div>
    <div id="map"></div>
    <table style="width:100%;">
      <tr>
        <td><div id="id_num_agents" style="text-align:center;"></div></td>
      </tr>
      <tr>
        <td><div id="id_called_agents" style="text-align:center;"></div></td>
      </tr>
      <tr>
        <td>
            <div id="id_list_all_agents"></div>
        </td>
      </tr>
    </table>
  </body>
</html>
