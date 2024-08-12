# Name: Steven Tran
# Student ID: 2111364

import csv  
import datetime  # Accessing date and time functions

# Class to represent each item
class Product:
    def __init__(self, ID=000000, manufacturer='unknown', category='unknown', price='unknown', service_date='undefined', damaged='no'):
        self.ID = ID
        self.manufacturer = manufacturer
        self.category = category
        self.price = price
        self.service_date = service_date
        self.damaged = damaged

# Function sorting
def sort_by_id(product):
    return product.ID
def sort_by_price(product):
    return product.price
def sort_by_service_date(product):
    return product.service_date
def sort_by_manufacturer(product):
    return product.manufacturer


# Dictionary to store products by ID
product_dict = {}  # Load data from CSV files
# List to store product categories
category_list = []

# Processing the manufacturer list
with open('ManufacturerList.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for line in reader:
        # if the item is damaged or not
        damaged = 'no'
        if line[3] != '':
            damaged = 'yes'

        product_id = line[0]
        manufacturer = line[1]
        category = line[2]

        category_list.append(category)
        # Populate dictionary with product details, using ID as key
        product_dict[product_id] = {}
        product_dict[product_id]['ID'] = product_id
        product_dict[product_id]['manufacturer'] = manufacturer
        product_dict[product_id]['category'] = category
        product_dict[product_id]['damaged'] = damaged

# Processing service dates
with open('ServiceDatesList.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for line in reader:
        product_id = line[0]
        date = line[1]
        # Update service date in the dictionary
        product_dict[product_id]['service_date'] = date

# Processing prices
with open('PriceList.csv') as file:
    reader = csv.reader(file, delimiter=',')
    for line in reader:
        product_id = line[0]
        price = line[1]
        # Update price in the dictionary
        product_dict[product_id]['price'] = float(price)

# Change dictionary data into a list of Product objects
product_list = []
for product in product_dict.values():
    product_list.append(Product(
        ID=product['ID'],
        manufacturer=product['manufacturer'],
        category=product['category'],
        price=product['price'],
        service_date=product['service_date'],
        damaged=product['damaged'],
    ))

# Generating full inventory list
product_list.sort(key=sort_by_manufacturer)

with open('FullInventory.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    for product in product_list:
        writer.writerow(
            [product.ID, product.manufacturer, product.category, product.price, product.service_date,
             product.damaged])
        
# Generating inventory lists by category
for category in category_list:

    items_in_category = []

    for product in product_list:
        if product.category == category:
            items_in_category.append(product)

    # Sort by ID
    items_in_category.sort(key=sort_by_id)

    # Create file name for each category
    category_file = category.replace(" ", "") + "Inventory.csv"
    with open(category_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for product in items_in_category:
            writer.writerow(
                [product.ID, product.manufacturer, product.price, product.service_date, product.damaged])

# List products with past service dates
outdated_products = []
for product in product_list:
    # Compare service date with today's date
    date = product.service_date.split("/")
    service_date = datetime.date(int(date[2]), int(date[0]), int(date[1]))
    if service_date < datetime.date.today():
        outdated_products.append(product)

# Sort outdated products by service date
outdated_products.sort(key=sort_by_service_date, reverse=True)

with open('PastServiceDateInventory.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    for product in outdated_products:
        writer.writerow([product.ID, product.manufacturer, product.price, product.service_date, product.damaged])

# List damaged products
damaged_products = []
for product in product_list:
    if product.damaged == 'yes':
        damaged_products.append(product)

# Sort damaged products by price
damaged_products.sort(key=sort_by_price, reverse=True)

with open('DamagedInventory.csv', mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    for product in damaged_products:
        writer.writerow([product.ID, product.manufacturer, product.category, product.price, product.service_date])
