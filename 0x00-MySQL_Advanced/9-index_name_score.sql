-- This script creates an index on a table(names) and the first letter
-- a column(name) and another column(score)
CREATE INDEX idx_name_first_score on names(name(1), score(1));
