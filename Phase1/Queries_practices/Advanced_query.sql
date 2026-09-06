-- 5. Top 5 customers by total spending
SELECT c.first_name, c.last_name, SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN payments p ON o.order_id = p.order_id
WHERE p.payment_status = 'completed'
GROUP BY c.customer_id
ORDER BY total_spent DESC
LIMIT 5;

-- 6. Best selling products (by quantity)
SELECT p.product_name, SUM(oi.quantity) AS total_sold
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id
ORDER BY total_sold DESC
LIMIT 10;

-- 7. Monthly revenue for last 12 months
SELECT 
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    SUM(p.amount) AS revenue
FROM orders o
JOIN payments p ON o.order_id = p.order_id
WHERE p.payment_status = 'completed'
    AND o.order_date >= DATE_SUB(NOW(), INTERVAL 12 MONTH)
GROUP BY month
ORDER BY month;

-- 8. Category-wise revenue
SELECT 
    pr.category,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount/100)) AS revenue
FROM order_items oi
JOIN products pr ON oi.product_id = pr.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status = 'delivered'
GROUP BY pr.category
ORDER BY revenue DESC;