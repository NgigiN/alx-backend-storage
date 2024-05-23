-- This script creates an index on the first letter of values of a column
CREATE INDEX idx_name_first ON names(name(1));
