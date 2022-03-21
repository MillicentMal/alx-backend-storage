-- creating trigger for orders

create trigger AFTER INSERT ON orders
for each row set items.quantity = items.quantity - orders.number;
