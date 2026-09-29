CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL,
    is_superuser BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS venues (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    capacity INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(1024),
    date DATE NOT NULL,
    location VARCHAR(255) NOT NULL,
    price DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS ticket_types (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(1024),
    price DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    event_id UUID NOT NULL,
    amount DOUBLE PRECISION NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    id UUID PRIMARY KEY,
    order_id UUID NOT NULL CONSTRAINT fk_order_items_order REFERENCES orders(id),
    ticket_type_id UUID NOT NULL,
    quantity INTEGER NOT NULL,
    price DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS payments (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    order_id UUID NOT NULL CONSTRAINT fk_payments_order REFERENCES orders(id),
    amount DOUBLE PRECISION NOT NULL,
    status VARCHAR(50) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_event_id ON orders(event_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_ticket_type_id ON order_items(ticket_type_id);
CREATE INDEX IF NOT EXISTS idx_payments_order_id ON payments(order_id);

-- Synthetic data only. Password values are placeholders, not production-usable credentials.
INSERT INTO users (
    id, username, email, password, firstname, lastname, is_active, is_superuser
) VALUES
    ('00000000-0000-4000-8000-000000000001', 'alex.rivera', 'alex.rivera@example.com', 'password123', 'Alex', 'Rivera', TRUE, TRUE),
    ('00000000-0000-4000-8000-000000000002', 'jordan.lee', 'jordan.lee@example.com', 'password321', 'Jordan', 'Lee', TRUE, FALSE),
    ('00000000-0000-4000-8000-000000000003', 'sam.patel', 'sam.patel@example.com', 'password456', 'Sam', 'Patel', TRUE, FALSE)
ON CONFLICT DO NOTHING;

INSERT INTO venues (id, name, address, capacity) VALUES
    ('10000000-0000-4000-8000-000000000001', 'The Ford', '2580 Cahuenga Blvd E, Los Angeles, CA', 1200),
    ('10000000-0000-4000-8000-000000000002', 'Canyon Theater', '25 Arts Plaza, Los Angeles, CA', 450),
    ('10000000-0000-4000-8000-000000000003', 'Valley Park', '800 Park Avenue, Northridge, CA', 5000)
ON CONFLICT DO NOTHING;

INSERT INTO events (id, name, description, date, location, price) VALUES
    ('20000000-0000-4000-8000-000000000001', 'Indie Sounds Live', 'An evening featuring emerging independent artists.', '2026-11-14', 'Northstar Hall', 45.00),
    ('20000000-0000-4000-8000-000000000002', 'Laugh Lines', 'A night of stand-up comedy from local performers.', '2026-12-05', 'Canyon Theater', 35.00),
    ('20000000-0000-4000-8000-000000000003', 'The Winter Play', 'A contemporary theater production.', '2027-01-22', 'Canyon Theater', 80.00),
    ('20000000-0000-4000-8000-000000000004', 'Summer Day Festival', 'A full day of live music and food.', '2027-06-19', 'Valley Park', 55.00)
ON CONFLICT DO NOTHING;

INSERT INTO ticket_types (id, name, description, price) VALUES
    ('30000000-0000-4000-8000-000000000001', 'General Admission', 'Standard event admission.', 45.00),
    ('30000000-0000-4000-8000-000000000002', 'VIP Admission', 'Premium seating and early entry.', 95.00),
    ('30000000-0000-4000-8000-000000000003', 'Comedy Admission', 'Reserved seating for comedy events.', 35.00),
    ('30000000-0000-4000-8000-000000000004', 'Theater Admission', 'Reserved seating for theater performances.', 80.00),
    ('30000000-0000-4000-8000-000000000005', 'Festival Admission', 'Single-day festival access.', 55.00)
ON CONFLICT DO NOTHING;

INSERT INTO orders (id, user_id, event_id, amount, status) VALUES
    ('40000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000000001', '20000000-0000-4000-8000-000000000001', 185.00, 'confirmed'),
    ('40000000-0000-4000-8000-000000000002', '00000000-0000-4000-8000-000000000002', '20000000-0000-4000-8000-000000000002', 105.00, 'confirmed'),
    ('40000000-0000-4000-8000-000000000003', '00000000-0000-4000-8000-000000000003', '20000000-0000-4000-8000-000000000003', 160.00, 'pending'),
    ('40000000-0000-4000-8000-000000000004', '00000000-0000-4000-8000-000000000001', '20000000-0000-4000-8000-000000000004', 55.00, 'payment_failed')
ON CONFLICT DO NOTHING;

INSERT INTO order_items (id, order_id, ticket_type_id, quantity, price) VALUES
    ('50000000-0000-4000-8000-000000000001', '40000000-0000-4000-8000-000000000001', '30000000-0000-4000-8000-000000000001', 2, 45.00),
    ('50000000-0000-4000-8000-000000000002', '40000000-0000-4000-8000-000000000001', '30000000-0000-4000-8000-000000000002', 1, 95.00),
    ('50000000-0000-4000-8000-000000000003', '40000000-0000-4000-8000-000000000002', '30000000-0000-4000-8000-000000000003', 3, 35.00),
    ('50000000-0000-4000-8000-000000000004', '40000000-0000-4000-8000-000000000003', '30000000-0000-4000-8000-000000000004', 2, 80.00),
    ('50000000-0000-4000-8000-000000000005', '40000000-0000-4000-8000-000000000004', '30000000-0000-4000-8000-000000000005', 1, 55.00)
ON CONFLICT DO NOTHING;

INSERT INTO payments (id, user_id, order_id, amount, status) VALUES
    ('60000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000000001', '40000000-0000-4000-8000-000000000001', 185.00, 'completed'),
    ('60000000-0000-4000-8000-000000000002', '00000000-0000-4000-8000-000000000002', '40000000-0000-4000-8000-000000000002', 105.00, 'completed'),
    ('60000000-0000-4000-8000-000000000003', '00000000-0000-4000-8000-000000000003', '40000000-0000-4000-8000-000000000003', 160.00, 'pending'),
    ('60000000-0000-4000-8000-000000000004', '00000000-0000-4000-8000-000000000001', '40000000-0000-4000-8000-000000000004', 55.00, 'failed')
ON CONFLICT DO NOTHING;

