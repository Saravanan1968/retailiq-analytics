-- SELECT * FROM customers LIMIT 250;

-- SELECT * FROM customers where state = "Tamil Nadu";

-- select product_name, category, price from products order by price desc;

-- select status , count(*) as total_orders from orders group by 1;
select sum(amount) as total_revenue from payments where payment_status = "completed";
