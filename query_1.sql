SELECT s.name AS name, AVG(m.mark) AS average_mark FROM students s
LEFT JOIN marks m ON s.id = m.student_id
GROUP BY name
ORDER BY average_mark DESC LIMIT 5;