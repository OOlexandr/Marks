SELECT s.name
FROM students s 
LEFT JOIN groups g ON g.id = s.group_id 
WHERE g.id = @group_number;