SELECT * FROM agent_list;

SELECT * FROM user_list;

SELECT * FROM agent_current_info;

SELECT * FROM user_requests;

SELECT * FROM agent_calls;

--For each agent return their last call status and who has called them when
SELECT 
  final_calls.agent_id,  
  current.lat_data, 
  current.long_data, 
  final_calls.call_flag, 
  final_calls.user_that_called, 
  final_calls.call_timestamp, 
  final_calls.lat_data, 
  final_calls.long_data,
  people.user_agent_type
FROM 
agent_current_info AS current, 
( ( SELECT 
      u.`agent_id`, 
      u.`lat_data`, 
      u.`long_data`, 
      u.`call_flag`, 
      u.`user_that_called`, 
      u.`call_timestamp` 
    FROM agent_calls AS u 
INNER JOIN 
  ( SELECT 
      `agent_id`, 
      MAX(`call_timestamp`) AS time_stamp 
    FROM agent_calls 
    GROUP BY `agent_id` ) 
  AS q ON u.`agent_id` = q.`agent_id` AND u.`call_timestamp` = q.`time_stamp` ) 
AS final_calls ),
operator_list as people
WHERE final_calls.agent_id = current.agent_id
AND final_calls.agent_id = people.agent_id
AND current.online_flag = 1;

SELECT * FROM agent_current_info,operator_list WHERE online_flag = 1 AND user_agent_type=1 AND agent_current_info.agent_id=operator_list.agent_id