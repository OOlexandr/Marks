SELECT s.name, m.mark
FROM marks m 
LEFT JOIN students s ON m.student_id = s.id 
LEFT JOIN groups g ON s.group_id = g.id 
LEFT JOIN subjects sub ON m.subject_id = sub.id 
WHERE g.id = @group_number
AND sub.name = @subject 
AND m.mark_date = (
	SELECT MAX(m2.mark_date)
	FROM marks m2
	LEFT JOIN subjects sub2 ON m2.subject_id = sub2.id
	LEFT JOIN students s2 ON m2.student_id = s2.id 
	LEFT JOIN groups g2 ON s2.group_id = g2.id 
	WHERE sub2.name = @subject
	AND g2.id = @group_number);