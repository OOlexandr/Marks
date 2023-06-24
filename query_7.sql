SELECT s.name, m.mark
FROM marks m
LEFT JOIN students s ON m.student_id = s.id 
LEFT JOIN subjects sub ON m.subject_id = sub.id 
LEFT JOIN groups g ON s.group_id = g.id 
WHERE g.id = 1 
AND sub.name = "language";