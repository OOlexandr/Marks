SELECT g.id as group_number, AVG(m.mark) AS average_mark
FROM groups g
LEFT JOIN students s ON s.group_id = g.id
LEFT JOIN marks m ON m.student_id = s.id 
LEFT JOIN subjects sub ON m.subject_id = sub.id
WHERE sub.name = @subject
GROUP BY group_number;