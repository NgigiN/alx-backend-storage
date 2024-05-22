-- This script should list all bands with Glam Rock
-- their main style, ranked by longetivity
SELECT band_name,
  (2022 - origin) AS lifespan
FROM metal_bands
where style = 'Glam rock'
ORDER BY lifespan DESC;