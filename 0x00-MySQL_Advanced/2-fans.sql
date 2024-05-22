-- This script ranks country of origin of bands
-- ordered by the number of non-unique fans
SELECT origin,
  SUM(fans) AS total_fans
from metal_bands
GROUP BY origin
ORDER BY total_fans DESC;