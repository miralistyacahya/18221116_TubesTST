CREATE TABLE cakes (
    cake_id int AUTO_INCREMENT PRIMARY KEY,
    cake_name varchar(255) NOT NULL,
    template_img varchar(255),
    created_at timestamp DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO cakes (cake_name, template_img) VALUES
    ('Red Velvet Sponge Cake', 'b5b7620a880375e1.jpg'),
    ('Lotus Cheese Cake', 'b5b7620a880375e1.jpg'),
    ('Original Cheese Cake', 'b5b7620a880375e1.jpg');