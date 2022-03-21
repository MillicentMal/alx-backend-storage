-- Pulling data from existing table
SELECT band_name, TIMESTAMPDIFF(YEAR, split, formed) AS lifespan FROM metal_bands  WHERE style='Glam rock' ORDER BY lifespan DESC;
