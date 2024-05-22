-- This script should list all bands with Glam Rock
-- their main style, ranked by longetivity
SELECT band_name,
  (IFNULL(split, '2020') - formed) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
ORDER BY lifespan DESC;