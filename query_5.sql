SELECT s.name
FROM subjects s
LEFT JOIN teachers t ON t.id = s.teacher_id 
WHERE t.name = @teacher;