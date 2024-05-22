-- This script should list all bands with Glam Rock
-- their main style, ranked by longetivity
SELECT band_name,
  CASE
    WHEN split IS NULL THEN 2022 - formed
    ELSE split - formed
  END AS lifespan
FROM metal_bands
where style = 'Glam rock'
ORDER BY lifespan DESC;