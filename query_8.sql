SELECT AVG(m.mark) as average_mark
FROM teachers t 
LEFT JOIN subjects s ON t.id = s.teacher_id 
LEFT JOIN marks m ON s.id = m.subject_id 
WHERE t.name = @teacher;