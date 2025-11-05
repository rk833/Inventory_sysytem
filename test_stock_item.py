from stock_item import StockItem
from nav_sys import NavSys

# Test StockItem class
print("Testing StockItem class:")
item1 = StockItem("W101", 10, 99.99)
print("Creating a stock with 10 units Unknown item, price 99.99 each, and item code W101")
print("Printing item stock information:")
print(item1)

print("\nIncreasing 10 more units")
item1.increase_stock(10)
print("Printing item stock information:")
print(item1)

print("\nSold 2 units")
item1.sell_stock(2)
print("Printing item stock information:")
print(item1)

print("\nSet new price 100.99 per unit")
item1.set_price(100.99)
print("Printing item stock information:")
print(item1)

print("\nIncreasing 0 more units")
item1.increase_stock(0)

# Test NavSys class
print("\nTesting NavSys class:")
nav1 = NavSys("NS101", 10, 99.99, "TomTom")
print("Creating a stock with 10 units Navigation system, price 99.99, item code NS101, and brand TomTom")
print("Printing item stock information:")
print(nav1)

print("\nIncreasing 10 more units")
nav1.increase_stock(10)
print("Printing item stock information:")
print(nav1)

print("\nSold 2 units")
nav1.sell_stock(2)
print("Printing item stock information:")
print(nav1)

print("\nSet new price 100.99 per unit")
nav1.set_price(100.99)
print("Printing item stock information:")
print(nav1)

print("\nIncreasing 0 more units")
nav1.increase_stock(0)
