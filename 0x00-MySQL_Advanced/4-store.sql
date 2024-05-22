-- This script creates a trigger that decreases an item's
-- quantitiy after adding a new order
DROP TRIGGER IF EXISTS reduce_quantity;
DELIMITER $$ CREATE TRIGGER reduce_quantity
AFTER
INSERT ON orders FOR EACH ROW BEGIN
UPDATE items
SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;
END $$ DELIMITER;