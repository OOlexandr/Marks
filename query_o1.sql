SELECT AVG(m.mark)
FROM subjects sub 
LEFT JOIN marks m ON sub.id = m.subject_id 
LEFT JOIN students s ON m.student_id = s.id 
LEFT JOIN teachers t ON sub.teacher_id = t.id
WHERE s.name = @student AND t.name = @teacher;