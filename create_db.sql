CREATE TABLE categories (
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	description VARCHAR(500),
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	update_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

	CONSTRAINT ck_categories_name_not_null CHECK (LENGTH(TRIM(name)) > 0)
);

CREATE TABLE sellers (
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	email VARCHAR(250) NOT NULL,
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
	update_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

	CONSTRAINT ck_sellers_name_not_null CHECK (LENGTH(TRIM(name)) > 0)
);

CREATE UNIQUE INDEX uq_sellers_email_lower ON sellers (LOWER(email));

CREATE TABLE products(
	id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	description VARCHAR(2000),
	price NUMERIC(12, 2) NOT NULL,
	stock_quantity INT NOT NULL DEFAULT 0,
	is_active BOOLEAN NOT NULL DEFAULT TRUE,
	category_id INT NOT NULL,
	seller_id INT NOT NULL,
	created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

	CONSTRAINT ck_products_name_not_empty CHECK (LENGTH(TRIM(name)) > 0),
	
	CONSTRAINT ck_products_price_positive CHECK (price > 0),

    CONSTRAINT ck_products_stock_non_negative CHECK (stock_quantity >= 0),

    CONSTRAINT fk_products_category
        FOREIGN KEY (category_id)
        REFERENCES categories(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_products_seller
        FOREIGN KEY (seller_id)
        REFERENCES sellers(id)
        ON DELETE RESTRICT
);

CREATE INDEX ix_products_category_id ON products(category_id);
CREATE INDEX ix_products_seller_id ON products(seller_id);






