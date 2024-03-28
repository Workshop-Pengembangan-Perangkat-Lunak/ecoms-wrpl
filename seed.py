import pandas as pd
from ecoms.models import *

# Create User and Customer
df = pd.read_csv('seed_data/User.csv')
for index, row in df.iterrows():
    user = User(username=row['first_name'] +
                row['last_name'], password=row['last_name'])
    user.save()
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
