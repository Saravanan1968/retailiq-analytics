#creating database
create database retailiq;
use retailiq;

#creating customers table
create table customers (
	customer_id INT auto_increment primary KEY,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    email varchar(100) unique not null,
    phone varchar(20),
    city varchar(100),
    state varchar(100),
    country varchar(50) default'India',
    created_at datetime default current_timestamp
);

#creating products table
create table products (
	product_id INT auto_increment primary KEY,
    product_name varchar(150) not null,
    category varchar(100),
    brand varchar(100),
    price decimal(10,2) not null,
    cost_price decimal(10,2) not null,
    created_at datetime default current_timestamp
);

#creating inventry table
create table inventory (
	inventory_id int auto_increment primary key,
    product_id int not null,
    quantity_in_stock int default 0,
    last_updated datetime default current_timestamp on update current_timestamp,
    foreign key(product_id) references products(product_id)
);


#creating orders table

create table orders(
	order_id int auto_increment primary key,
    customer_id int not null,
    order_date datetime default current_timestamp,
    status enum('pending','processing','shipped','delivered','cancelled') default'pending',
    total_amount decimal(10,2),
    shipping_city varchar(100),
    foreign key(customer_id) references customers(customer_id)
);


#creating order items table
create table order_items(
	item_id int auto_increment primary key,
    order_id int not null,
    product_id int not null,
    quantity int not null,
    unit_price decimal(10,2) not null,
    discount decimal(5,2) default 0.0,
    foreign key (order_id) references orders(order_id),
    foreign key (product_id) references products(product_id)
);

#creating payments table
create table payments(
	payment_id int auto_increment primary key,
    order_id int not null,
    payment_date datetime default current_timestamp,
    amount decimal(10,2) not null,
    payment_method enum('credit_card', 'debit_card', 'upi', 'net_banking', 'cod') not null,
    payment_status enum ('pending', 'completed', 'failed', 'refunded' ) default 'pending',
    foreign key (order_id) references orders(order_id)
);


    