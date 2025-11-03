"""
Database Initialization and Sample Data (Simple Version)
"""
import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.core.database import engine, Base, AsyncSessionLocal
from app.models import Menu, MenuOption, Order, OrderItem, OrderStatus
from datetime import datetime

async def init_database():
    """Initialize database"""
    print("\n" + "="*60)
    print("OrderBean Database Initialization")
    print("="*60)
    print()
    
    try:
        # 1. Create tables
        print("[1/2] Creating database tables...")
        async with engine.begin() as conn:
            # Drop existing tables (development only!)
            await conn.run_sync(Base.metadata.drop_all)
            # Create new tables
            await conn.run_sync(Base.metadata.create_all)
        print("   OK: Tables created!")
        print()
        
        # 2. Create sample data
        print("[2/2] Creating sample data...")
        async with AsyncSessionLocal() as session:
            # Menu data
            menus = [
                Menu(
                    name="Americano",
                    description="Strong espresso with water",
                    price=4000,
                    image_url="/images/americano.jpg",
                    stock=100,
                    is_available=True
                ),
                Menu(
                    name="Cafe Latte",
                    description="Smooth milk with espresso",
                    price=4500,
                    image_url="/images/latte.jpg",
                    stock=100,
                    is_available=True
                ),
                Menu(
                    name="Cappuccino",
                    description="Perfect balance of espresso and milk foam",
                    price=4500,
                    image_url="/images/cappuccino.jpg",
                    stock=100,
                    is_available=True
                ),
                Menu(
                    name="Vanilla Latte",
                    description="Latte with sweet vanilla syrup",
                    price=5000,
                    image_url="/images/vanilla-latte.jpg",
                    stock=80,
                    is_available=True
                ),
                Menu(
                    name="Caramel Macchiato",
                    description="Sweet harmony of milk and caramel",
                    price=5500,
                    image_url="/images/caramel-macchiato.jpg",
                    stock=80,
                    is_available=True
                ),
            ]
            
            session.add_all(menus)
            await session.flush()  # Flush to get IDs
            
            print(f"   OK: Created {len(menus)} menus!")
            
            # Option data
            options = []
            for menu in menus:
                # Size options
                options.extend([
                    MenuOption(menu_id=menu.id, name="Size: Regular", additional_price=0),
                    MenuOption(menu_id=menu.id, name="Size: Large", additional_price=500),
                ])
                # Shot options
                options.extend([
                    MenuOption(menu_id=menu.id, name="Extra Shot: 1 Shot", additional_price=500),
                    MenuOption(menu_id=menu.id, name="Extra Shot: 2 Shots", additional_price=1000),
                ])
                # Temperature options
                options.extend([
                    MenuOption(menu_id=menu.id, name="Temperature: HOT", additional_price=0),
                    MenuOption(menu_id=menu.id, name="Temperature: ICE", additional_price=0),
                ])
            
            session.add_all(options)
            print(f"   OK: Created {len(options)} options!")
            
            # Test order data
            test_order = Order(
                order_number="ORD-20251103-001",
                total_amount=12500,
                status=OrderStatus.RECEIVED
            )
            session.add(test_order)
            await session.flush()
            
            # Order items
            order_items = [
                OrderItem(
                    order_id=test_order.id,
                    menu_id=menus[0].id,  # Americano
                    quantity=2,
                    unit_price=4000,
                    subtotal=8000
                ),
                OrderItem(
                    order_id=test_order.id,
                    menu_id=menus[1].id,  # Cafe Latte
                    quantity=1,
                    unit_price=4500,
                    subtotal=4500
                ),
            ]
            
            # Update total
            test_order.total_amount = sum(item.subtotal for item in order_items)
            
            session.add_all(order_items)
            print(f"   OK: Created test order!")
            
            # Commit
            await session.commit()
        
        print()
        print("="*60)
        print("SUCCESS: Database initialization complete!")
        print("="*60)
        print()
        print("Created data:")
        print(f"   - Menus: {len(menus)}")
        print(f"   - Options: {len(options)}")
        print(f"   - Orders: 1 (test)")
        print()
        print("Start the server:")
        print("   python -m uvicorn app.main:app --reload")
        print()
        print("API Documentation:")
        print("   http://localhost:8000/api/docs")
        print()
        
        return True
        
    except Exception as e:
        print(f"\nERROR: Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        await engine.dispose()


def main():
    """Main function"""
    try:
        success = asyncio.run(init_database())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nWARNING: Initialization interrupted.")
        sys.exit(1)


if __name__ == "__main__":
    main()

