CREATE TABLE cakes (
    cake_id int AUTO_INCREMENT PRIMARY KEY,
    cake_name varchar(255) NOT NULL,
    template_img varchar(255),
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customers (
    customer_id int AUTO_INCREMENT PRIMARY KEY,
    customer_name varhcar(255) NOT NULL,
    phone varchar(255) NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE orders (
    order_id int AUTO_INCREMENT PRIMARY KEY,
    customer_id int, 
    cake_id int,
    order_date date,
    pickup_date date,
    order_status ENUM('pickup', 'delivery'),
    addr varchar(255),
    cake_img varchar(255),
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (cake_id) REFERENCES cakes(cake_id)
);
    
INSERT INTO cakes (cake_name, template_img) VALUES
    ('Red Velvet Sponge Cake', 'b5b7620a880375e1.jpg'),
    ('Lotus Cheese Cake', 'b5b7620a880375e1.jpg'),
    ('Original Cheese Cake', 'b5b7620a880375e1.jpg');

INSERT INTO customers(customer_name, phone) VALUES
    ('pipo', '0812345667');

INSERT INTO orders(customer_id, cake_id, order_date, pickup_date, order_status, addr, cake_img) VALUES
    (1, 1, '2023-03-12', '2023-03-21', 'Delivery', 'Jl. Dago Asri III No. 21', '0f4b49b8d1863d55.jpg');
