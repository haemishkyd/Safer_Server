SELECT
  final_calls.agent_id,
  current.lat_data,
  current.long_data,
  final_calls.call_flag,
  final_calls.user_that_called,
  final_calls.call_timestamp,
  final_calls.lat_data,
  final_calls.long_data
FROM
  agent_current_info AS current,
  (
    (
    SELECT
      u.`agent_id`,
      u.`lat_data`,
      u.`long_data`,
      u.`call_flag`,
      u.`user_that_called`,
      u.`call_timestamp`
    FROM
      agent_calls AS u
    INNER JOIN
      (
      SELECT
        `agent_id`,
        MAX(`call_timestamp`) AS time_stamp
      FROM
        agent_calls
      GROUP BY
        `agent_id`
      ) AS q ON u.`agent_id` = q.`agent_id` AND u.`call_timestamp` = q.`time_stamp`
    ) AS final_calls
  )
WHERE final_calls.agent_id = current.agent_id