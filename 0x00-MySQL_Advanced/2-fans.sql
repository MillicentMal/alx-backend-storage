-- Pulling data from existing table
SELECT origin, SUM(fans) AS nb_fans  GROUP BY origin ORDER BY fans DESC;
