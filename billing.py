import gspread
from database import load_price_from_db

sa = gspread.service_account(filename='academic-pier-380806-d883a15b440a.json')
sh = sa.open("Enactus")

products_for_inventory = []
for row in load_price_from_db():
  products_for_inventory.append(row['product'])

prices = []
for row in load_price_from_db():
  prices.append(row['price'])

prices_for_schemes = [160 / 3, 100, 50 / 3, 80 / 3]

products_for_schemes = ["scrunchie*3", "zipper*3", "pencil*3", "pen*3"]


def price_of_product(product, num):
  if num != 3:
    if product in products_for_inventory:
      index_1 = products_for_inventory.index(product)
      return prices[index_1]
    else:
      return -1

  else:
    if f'{product}*3' in products_for_schemes:
      index_1 = products_for_schemes.index(f'{product}*3')
      return prices_for_schemes[index_1]


def auto_inventory_update(product, quantities):
  update_inventory_by_record(product, quantities, operation=0)


def update_inventory_by_record(item, quantity, operation):
  rowcount = products_for_inventory.index(item) + 2
  if operation == 1:
    increment(quantity, rowcount)
  elif operation == 0:
    decrement(quantity, rowcount)


def increment(quantity, row_count):
  sheet = sh.worksheet("inventory")
  current = int(sheet.cell(row_count, 3).value)
  sheet.update_cell(row_count, 3, current + quantity)


def decrement(quantity, row_count):
  sheet = sh.worksheet("inventory")
  current = int(sheet.cell(row_count, 3).value)
  sheet.update_cell(row_count, 3, current - quantity)


def calculatetotal(items):
  total = 0
  for item in items:
    total += item['price'] * item['quantity']
  return total


def next_available_row(worksheet):
  str_len = len(worksheet.get_all_values())
  return str_len + 1


def generatebill(items, total, naam, contacts):
  sheet = sh.worksheet("billing")
  next_row = next_available_row(sheet)
  row_count = next_row
  sheet.update_cell(row_count + 1, 1, naam)
  sheet.update_cell(row_count + 1, 2, contacts)
  for item in items:
    sheet.update_cell(row_count + 1, 3, item['product'])
    sheet.update_cell(row_count + 1, 4, item['quantity'])
    sheet.update_cell(row_count + 1, 5, int(item['price']))
    sheet.update_cell(row_count + 1, 6, item['price'] * item['quantity'])
    row_count += 1
  sheet.update_cell(row_count + 1, 7, total)


def calculate_bill_and_add_to_sheets(name_contact_product_quantity):
  customer = name_contact_product_quantity['name']
  contact = name_contact_product_quantity['contact']
  items = []
  for item in name_contact_product_quantity:
    if item in products_for_inventory:
      quantity = int(name_contact_product_quantity[item])
      if quantity != 0:
        price1 = price_of_product(item, quantity)
        items.append({'product': item, 'price': price1, 'quantity': quantity})
        auto_inventory_update(item, quantity)

  total = calculatetotal(items)
  generatebill(items, total, customer, contact)
