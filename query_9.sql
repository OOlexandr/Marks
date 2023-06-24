SELECT sub.name
FROM subjects sub 
LEFT JOIN marks m ON sub.id = m.subject_id 
LEFT JOIN students s ON m.student_id = s.id 
WHERE s.name = @student
GROUP BY sub.name;