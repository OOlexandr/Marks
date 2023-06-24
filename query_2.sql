SELECT s.name AS name, AVG(m.mark) as average_mark
FROM students AS s 
LEFT JOIN marks as m ON s.id = m.student_id
LEFT JOIN subjects as sub ON m.subject_id = sub.id
WHERE sub.name = @subject
ORDER BY average_mark DESC 
LIMIT 1;