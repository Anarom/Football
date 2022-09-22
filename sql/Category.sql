Select 
	event_qualifiers.name AS text,
	count(*) AS "Total",
	count(*) FILTER (WHERE NOT is_goal) AS "Shots", 
	count(*) FILTER (WHERE is_goal AND NOT is_own_goal) AS "Goals",
	count(*) FILTER (WHERE is_goal and is_own_goal) AS "Own Goals"
FROM
	core.events
JOIN
	core.event_qualifiers ON event_qualifiers.id = events.zone
JOIN
	core.event_types ON event_types.id = events.type
WHERE
	event_types.name IN ('missed_shots','shot_on_post', 'saved_shot', 'goal')
GROUP BY
	text