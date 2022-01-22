-- Pulling data from existing table
SELECT origin, SUM(fans) AS nb_fans FROM metal_bands  GROUP BY origin ORDER BY fans DESC;
