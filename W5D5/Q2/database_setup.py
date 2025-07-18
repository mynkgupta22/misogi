import sqlite3
import random
from datetime import datetime, timedelta

def create_database():
    """Create SQLite database with proper schema and sample data"""
    
    # Connect to database (creates if doesn't exist)
    conn = sqlite3.connect('commerce_data.db')
    cursor = conn.cursor()
    
    # Create tables
    create_tables(cursor)
    
    # Insert sample data
    insert_sample_data(cursor)
    
    conn.commit()
    conn.close()
    
    print("✅ Database created successfully with sample data!")

def create_tables(cursor):
    """Create all necessary tables for the commerce platform"""
    
    # Platforms table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS platforms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL UNIQUE,
            commission DECIMAL(5,2) NOT NULL,
            delivery_time VARCHAR(50) NOT NULL,
            coverage_area VARCHAR(200) DEFAULT 'Pan India',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            parent_id INTEGER,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES categories(id)
        )
    ''')
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200) NOT NULL,
            category_id INTEGER NOT NULL,
            brand VARCHAR(100),
            unit VARCHAR(50),
            description TEXT,
            barcode VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')
    
    # Current prices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS current_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            platform_id INTEGER NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            mrp DECIMAL(10,2) NOT NULL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (platform_id) REFERENCES platforms(id),
            UNIQUE(product_id, platform_id)
        )
    ''')
    
    # Price history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            platform_id INTEGER NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (platform_id) REFERENCES platforms(id)
        )
    ''')
    
    # Discounts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS discounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            platform_id INTEGER NOT NULL,
            discount_percent DECIMAL(5,2) NOT NULL,
            discount_type VARCHAR(50) DEFAULT 'percentage',
            start_date TIMESTAMP NOT NULL,
            end_date TIMESTAMP NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (platform_id) REFERENCES platforms(id)
        )
    ''')
    
    # Availability table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS availability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            platform_id INTEGER NOT NULL,
            is_available BOOLEAN DEFAULT 1,
            stock_quantity INTEGER DEFAULT 0,
            estimated_delivery VARCHAR(50),
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (platform_id) REFERENCES platforms(id),
            UNIQUE(product_id, platform_id)
        )
    ''')
    
    # Search queries log table (for analytics)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT NOT NULL,
            generated_sql TEXT,
            result_type VARCHAR(50),
            response_time_ms INTEGER,
            user_session VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Popular products table (for analytics)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS popular_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            search_count INTEGER DEFAULT 1,
            conversion_rate DECIMAL(5,2) DEFAULT 0.0,
            last_searched TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id),
            UNIQUE(product_id)
        )
    ''')
    
    print("📊 Database tables created successfully!")

def insert_sample_data(cursor):
    """Insert comprehensive sample data"""
    
    # Insert platforms
    platforms = [
        ("Blinkit", 15.0, "10-15 min"),
        ("Zepto", 12.0, "10-15 min"),
        ("Instamart", 18.0, "15-30 min"),
        ("BigBasket Now", 20.0, "15-45 min"),
        ("Dunzo", 22.0, "20-45 min")
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO platforms (name, commission, delivery_time) 
        VALUES (?, ?, ?)
    ''', platforms)
    
    # Insert categories
    categories = [
        ("Vegetables", None, "Fresh vegetables and greens"),
        ("Fruits", None, "Fresh seasonal fruits"),
        ("Dairy", None, "Milk, curd, cheese and dairy products"),
        ("Snacks", None, "Chips, biscuits and snack items"),
        ("Beverages", None, "Drinks and beverages"),
        ("Household", None, "Cleaning and household items"),
        ("Personal Care", None, "Personal hygiene and care products")
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO categories (name, parent_id, description) 
        VALUES (?, ?, ?)
    ''', categories)
    
    # Insert products
    products = [
        # Vegetables (category_id: 1)
        ("Onions", 1, "Local", "kg", "Fresh red onions", "VEG001"),
        ("Tomatoes", 1, "Local", "kg", "Fresh tomatoes", "VEG002"),
        ("Potatoes", 1, "Local", "kg", "Fresh potatoes", "VEG003"),
        ("Carrots", 1, "Local", "kg", "Fresh carrots", "VEG004"),
        ("Spinach", 1, "Local", "bunch", "Fresh spinach leaves", "VEG005"),
        
        # Fruits (category_id: 2)
        ("Bananas", 2, "Local", "dozen", "Fresh bananas", "FRT001"),
        ("Apples", 2, "Kashmir", "kg", "Kashmir apples", "FRT002"),
        ("Oranges", 2, "Nagpur", "kg", "Nagpur oranges", "FRT003"),
        ("Mangoes", 2, "Alphonso", "kg", "Alphonso mangoes", "FRT004"),
        ("Grapes", 2, "Local", "kg", "Fresh grapes", "FRT005"),
        
        # Dairy (category_id: 3)
        ("Milk", 3, "Amul", "1L", "Fresh toned milk", "DRY001"),
        ("Curd", 3, "Amul", "500g", "Fresh curd", "DRY002"),
        ("Paneer", 3, "Amul", "200g", "Fresh paneer", "DRY003"),
        ("Butter", 3, "Amul", "100g", "Fresh butter", "DRY004"),
        
        # Snacks (category_id: 4)
        ("Chips", 4, "Lays", "pack", "Classic salted chips", "SNK001"),
        ("Biscuits", 4, "Parle G", "pack", "Glucose biscuits", "SNK002"),
        ("Cookies", 4, "Britannia", "pack", "Chocolate cookies", "SNK003"),
        
        # Beverages (category_id: 5)
        ("Coca Cola", 5, "Coca Cola", "500ml", "Soft drink", "BEV001"),
        ("Water Bottle", 5, "Bisleri", "1L", "Mineral water", "BEV002"),
        ("Orange Juice", 5, "Real", "1L", "Fresh orange juice", "BEV003")
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO products (name, category_id, brand, unit, description, barcode) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', products)
    
    # Get inserted data for generating prices and other dependent data
    cursor.execute("SELECT id FROM platforms")
    platform_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM products")
    product_ids = [row[0] for row in cursor.fetchall()]
    
    # Base prices for products
    base_prices = {
        1: 45,   # Onions
        2: 50,   # Tomatoes
        3: 30,   # Potatoes
        4: 60,   # Carrots
        5: 25,   # Spinach
        6: 40,   # Bananas
        7: 150,  # Apples
        8: 80,   # Oranges
        9: 200,  # Mangoes
        10: 120, # Grapes
        11: 60,  # Milk
        12: 45,  # Curd
        13: 80,  # Paneer
        14: 50,  # Butter
        15: 20,  # Chips
        16: 10,  # Biscuits
        17: 25,  # Cookies
        18: 40,  # Coca Cola
        19: 20,  # Water
        20: 80   # Orange Juice
    }
    
    # Insert current prices
    price_data = []
    for product_id in product_ids:
        base_price = base_prices.get(product_id, 50)  # Default price if not found
        for platform_id in platform_ids:
            # Add platform-specific price variation
            price_variation = random.uniform(0.8, 1.3)
            current_price = round(base_price * price_variation, 2)
            mrp = round(current_price * 1.2, 2)
            
            price_data.append((product_id, platform_id, current_price, mrp))
    
    cursor.executemany('''
        INSERT OR IGNORE INTO current_prices (product_id, platform_id, price, mrp) 
        VALUES (?, ?, ?, ?)
    ''', price_data)
    
    # Insert price history
    history_data = []
    for product_id in product_ids:
        for platform_id in platform_ids:
            # Get current price for this product-platform combo
            cursor.execute('''
                SELECT price FROM current_prices 
                WHERE product_id = ? AND platform_id = ?
            ''', (product_id, platform_id))
            result = cursor.fetchone()
            if result:
                current_price = result[0]
                
                # Generate historical prices for last 30 days
                for days_ago in range(1, 31):
                    historical_price = current_price * random.uniform(0.9, 1.1)
                    recorded_date = datetime.now() - timedelta(days=days_ago)
                    history_data.append((product_id, platform_id, round(historical_price, 2), recorded_date))
    
    cursor.executemany('''
        INSERT INTO price_history (product_id, platform_id, price, recorded_at) 
        VALUES (?, ?, ?, ?)
    ''', history_data)
    
    # Insert discounts
    discount_data = []
    # Create discounts for random products
    discount_products = random.sample(product_ids, min(15, len(product_ids)))
    
    for product_id in discount_products:
        platform_id = random.choice(platform_ids)
        discount_percent = random.choice([10, 15, 20, 25, 30, 35, 40, 50])
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now() + timedelta(days=7)
        
        discount_data.append((product_id, platform_id, discount_percent, start_date, end_date, 1))
    
    cursor.executemany('''
        INSERT INTO discounts (product_id, platform_id, discount_percent, start_date, end_date, is_active) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', discount_data)
    
    # Insert availability data
    availability_data = []
    for product_id in product_ids:
        for platform_id in platform_ids:
            is_available = random.choice([1, 1, 1, 1, 0])  # 80% availability
            stock_quantity = random.randint(0 if not is_available else 10, 100)
            delivery_time = random.choice(["10-15 min", "15-30 min", "30-45 min"])
            
            availability_data.append((product_id, platform_id, is_available, stock_quantity, delivery_time))
    
    cursor.executemany('''
        INSERT OR IGNORE INTO availability (product_id, platform_id, is_available, stock_quantity, estimated_delivery) 
        VALUES (?, ?, ?, ?, ?)
    ''', availability_data)
    
    print("💾 Sample data inserted successfully!")
    
    # Create indexes for better performance
    create_indexes(cursor)

def create_indexes(cursor):
    """Create indexes for better query performance"""
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)",
        "CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id)",
        "CREATE INDEX IF NOT EXISTS idx_current_prices_product ON current_prices(product_id)",
        "CREATE INDEX IF NOT EXISTS idx_current_prices_platform ON current_prices(platform_id)",
        "CREATE INDEX IF NOT EXISTS idx_discounts_active ON discounts(is_active)",
        "CREATE INDEX IF NOT EXISTS idx_discounts_product_platform ON discounts(product_id, platform_id)",
        "CREATE INDEX IF NOT EXISTS idx_availability_product_platform ON availability(product_id, platform_id)",
        "CREATE INDEX IF NOT EXISTS idx_price_history_product ON price_history(product_id)",
        "CREATE INDEX IF NOT EXISTS idx_search_queries_created ON search_queries(created_at)"
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)
    
    print("🔍 Database indexes created for optimal performance!")

def get_database_stats():
    """Get statistics about the database"""
    conn = sqlite3.connect('commerce_data.db')
    cursor = conn.cursor()
    
    stats = {}
    
    tables = ['platforms', 'categories', 'products', 'current_prices', 'discounts', 'availability', 'price_history']
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        stats[table] = cursor.fetchone()[0]
    
    conn.close()
    return stats

if __name__ == "__main__":
    create_database()
    
    # Show stats
    stats = get_database_stats()
    print("\n📈 Database Statistics:")
    for table, count in stats.items():
        print(f"  • {table}: {count:,} records")
    
    print("\n🎉 Database setup complete! Ready for SQL agent queries.") 