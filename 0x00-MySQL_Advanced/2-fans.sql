-- Pulling data from existing table
SELECT origin, sum(fans) GROUP BY origin ORDER BY fans DESC;
