import pandas as pd
from ecoms.models import *
from supplier.models import Supplier
from supplier.models import Product as SupplierProduct
# Create User and Customer
df = pd.read_csv('seed_data/User.csv')
users=  []
for index, row in df.iterrows():
    user = User(username=row['first_name'] +
                row['last_name'], password=row['last_name'])
    users.append(user)
    user.save()
    user.save(using='supplier_db')
    customer = Customer(user=user, first_name=row['first_name'], last_name=row['last_name'],
                        gender=row['gender'], phone=row['phone'], address=row['street_address'])
    customer.save()

# Create Department
df = pd.read_csv('seed_data/dept.csv')
for index, row in df.iterrows():
    dept = Department(dept_name=row['dept_name'])
    dept.save()

# Create Products
df = pd.read_csv('seed_data/products.csv')
for index, row in df.iterrows():
    dept = Department.objects.get(id=row['department_id'])
    product = Product(department_id=dept, product_name=row['item_name'], buying_price=row['buying_price'],
                      selling_price=row['selling_price'], description=row['description'], product_image=row['image'], stock=row['stock'])
    product.save()

df = pd.read_csv('seed_data/product_supplier.csv')
for index, row in df.iterrows():
    supplier = Supplier(
                user=users[index], no_telp="12123", location="surakarta", no_rek="2131223")
    supplier.save(using='supplier_db')
  
    product = SupplierProduct(product_name=row['product_name'], product_description=row['product_description'], 
        product_category=row['product_category'], product_price=row['product_price'], stock_gudang=row['stock_gudang'], supplier=supplier)
    
    product.save(using='supplier_db')

#  insert product supplier lintang
user = User(username="lintang", password="lintang", email="lintang")
user.save(using='supplier_db')
supplier = Supplier(
                user=user, no_telp="12123", location="surakarta", no_rek="2131223")
supplier.save(using='supplier_db')
df = pd.read_csv('seed_data/product_supplier.csv')
for index, row in df.iterrows():
    user = User.objects.using(
        'supplier_db').get(username="lintang")
    
    
  
    product = SupplierProduct(product_name=row['product_name'], product_description=row['product_description'], 
        product_category=row['product_category'], product_price=row['product_price'], stock_gudang=row['stock_gudang'], supplier=supplier)
    
    product.save(using='supplier_db')