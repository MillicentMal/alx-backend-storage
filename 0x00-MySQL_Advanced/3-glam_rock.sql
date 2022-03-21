-- Pulling data from existing table
SELECT band_name, COALESCE(split, 2022) - formed AS lifespan FROM metal_bands  WHERE style like '%Glam rock%' ORDER BY lifespan DESC;
