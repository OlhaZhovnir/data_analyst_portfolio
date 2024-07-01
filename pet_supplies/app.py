#Importing necessary modules and functions
from main import (Base, session, PetSupplies, engine)
from sqlalchemy import desc
import csv
import time
import re
from colorama import init, Fore, Style

# Initializing colorama for colored output
init(autoreset=True)

# Function to display main menu and get user choice
def menu():
    while True:
        print('''
        \nWELCOME TO PRODUCT MANAGEMENT SYSTEM:
        \r1. Add product
        \r2. Search product (You can further edit product or delete product)
        \r3. Product analysis
        \r4. Exit ''')
        choice = input_choice = input('Enter your choice: ')
        if choice in ['1', '2', '3', '4']:
            return choice
        else:
            print(Fore.RED + 'Please choose a valid option (1-4).' + Style.RESET_ALL)

# Function to display submenu and get user choice
def submenu():
    while True:
        print('''
        \n1. Edit product information
        \r2. Delete product
        \r3. Return to main menu''')
        choice = input('Enter your choice: ')
        if choice in ['1', '2', '3']:
            return choice
        else:
            print(Fore.RED + 'Please choose a valid option (1-3).' + Style.RESET_ALL)

# Function to clean and validate product rating
def clean_rate(rate_str):
    try:
        rate_float = float(rate_str)
        return rate_float
    except ValueError:
        rate_float = None
        return rate_float

# Function to clean and validate URL
def clean_url(url):
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://' 
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,63}'  
        r'|localhost'  
        r'|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
        r'(?::\d+)?' 
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if url_pattern.match(url):
        return url
    else:
        return None

# Function to clean and validate price
def clean_price(price_str):
    price_str = price_str.replace('₹', '')
    try:
        price_float = float(price_str)
        return price_float
    except ValueError:
        return None

# Function to clean and validate product ID
def clean_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        input(Fore.RED + "Product ID must be a number." + Style.RESET_ALL)
        return
    else:
        if product_id in options:
            return product_id
        else:
            input(Fore.RED + 'No product with this ID found.' + Style.RESET_ALL)
            return

# Function to add products from CSV file to the database
def add_csv():
    with open('All Pet Supplies.csv') as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            product_in_db = session.query(PetSupplies).filter(PetSupplies.name == row[0]).one_or_none()
            if product_in_db == None:
                name = row[0]
                category = row[1]
                subcategory = row[2]
                image_url = row[3]
                product_url = row[4]
                rating = clean_rate(row[5])
                num_ratings = row[6]
                discount_price = clean_price(row[7])
                regular_price = clean_price(row[8])
                new_product = PetSupplies(name=name, category=category, subcategory=subcategory, image_url=image_url, product_url=product_url, rating=rating, num_ratings=num_ratings, discount_price=discount_price, regular_price=regular_price)
                session.add(new_product)
        session.commit()

# Main application function
def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == '1':
            # Getting input for new product
            name = input('Enter the name of product: ')
            category = input('Enter the category of product: ')
            subcategory = input('Enter the subcategory of product: ')

            # Input and validate image URL
            while True:
                image_url = input('Enter the image URL: ')
                if clean_url(image_url):
                    break
                else:
                    print(Fore.RED + 'Invalid URL format. Please enter a valid URL.')


            while True:
                product_url = input('Enter the product URL: ')
                if clean_url(product_url):
                    break
                else:
                    print(Fore.RED + 'Invalid URL format. Please enter a valid URL.' + Style.RESET_ALL)

            # Input and validate rating
            while True:
                rating = input('Enter the rating of the product (between 0.0 and 5.0): ')
                try:
                    rating = float(rating)
                    if 0.0 <= rating <= 5.0:
                        break
                    else:
                        print(Fore.RED + 'Invalid input. Rating should be between 0.0 and 5.0.' + Style.RESET_ALL)
                except ValueError:
                    print(Fore.RED + 'Invalid input. Rating should be a number.'+ Style.RESET_ALL)

            # Input and validate number of ratings
            while True:
                num_ratings = input('Enter the number of ratings received by the product: ')
                if not num_ratings.isdigit():
                    print(Fore.RED + 'Invalid input. Number of ratings should be an integer.' + Style.RESET_ALL)
                else:
                    num_ratings = int(num_ratings)
                    break

            while True:
                discount_price_input = input('Enter the discount price of the product: ')
                discount_price = clean_price(discount_price_input)
                if discount_price is not None:
                    break
                else:
                    print(Fore.RED + 'Invalid input. Discount price should be a number.' + Style.RESET_ALL)


            while True:
                regular_price_input = input('Enter the regular price of the product: ')
                regular_price = clean_price(regular_price_input)
                if regular_price is not None:
                    break
                else:
                    print(Fore.RED + 'Invalid input. Regular price should be a number.' + Style.RESET_ALL)

            new_product = PetSupplies(name=name, category=category, subcategory=subcategory, image_url=image_url,
                                       product_url=product_url, rating=rating, num_ratings=num_ratings,
                                       discount_price=discount_price, regular_price=regular_price)
            session.add(new_product)
            session.commit()
            print('Product added to database.')
            time.sleep(1.5)


        elif choice == '2':
            search_option = input(
                'Choose search option:\n1. Search by word in product name\n2. Search by product ID\nEnter your choice: ')
            if search_option == '1':
                search_term = input('Enter product name or keyword to search: ')
                products = session.query(PetSupplies).filter(PetSupplies.name.ilike(f'%{search_term}%')).all()
                if not products:
                    print("No product found.")
                else:
                    for product in products:
                        print(f"Selected Product: {product.name}")
            elif search_option == '2':
                id_option = [product.id for product in session.query(PetSupplies)]  # Get IDs directly

                while True:

                    print(f'\nId Options: {id_option}')

                    id_choice = clean_id(input('\nProduct Id: '), id_option)

                    if isinstance(id_choice, int):
                        break

                the_product = session.query(PetSupplies).filter(PetSupplies.id == id_choice).first()

                print(f"Selected Product: {the_product.name}")

            sub_choice = submenu()
            if sub_choice == '1':
                the_product.name = input('Enter new name: ')
                the_product.category = input('Enter new category: ')
                the_product.subcategory = input('Enter new subcategory: ')
                while True:
                    new_image_url = input('Enter new image URL: ')
                    if clean_url(new_image_url):
                        the_product.image_url = new_image_url
                        break
                    else:
                        print(Fore.RED + 'Invalid URL format. Please enter a valid URL.' + Style.RESET_ALL)

                while True:
                    new_product_url = input('Enter new product URL: ')
                    if clean_url(new_product_url):
                        the_product.product_url = new_product_url
                        break
                    else:
                        print(Fore.RED + 'Invalid URL format. Please enter a valid URL.' + Style.RESET_ALL)

                while True:
                    discount_price_input = input('Enter regular price of the product: ')
                    discount_price = clean_price(discount_price_input)
                    if discount_price is not None:
                        break
                    else:
                        print(Fore.RED + 'Invalid input. Discount price should be a number.' + Style.RESET_ALL)

                while True:
                    regular_price_input = input('Enter regular price of the product: ')
                    regular_price = clean_price(regular_price_input)
                    if regular_price is not None:
                        break
                    else:
                        print(Fore.RED + 'Invalid input. Regular price should be a number.' + Style.RESET_ALL)
                session.commit()
                print("Product updated successfully!")
                time.sleep(1.5)


            elif sub_choice == '2':
                session.delete(the_product)
                session.commit()
                print('Product Deleted')
                time.sleep(1.5)

            elif sub_choice == '3':
                pass  # Return to main menu

            print(session.dirty)

        elif choice == '3':
            top_rated_products = session.query(PetSupplies).order_by(desc(PetSupplies.rating),desc(PetSupplies.num_ratings)).limit(5).all()
            lowest_rating_products = session.query(PetSupplies).filter(PetSupplies.rating > 0).order_by(PetSupplies.rating).limit(5).all()
            best_discount_products = session.query(PetSupplies).filter(PetSupplies.discount_price != None).order_by(desc((PetSupplies.regular_price - PetSupplies.discount_price) / PetSupplies.regular_price)).limit(5).all()
            most_expensive_products = session.query(PetSupplies).order_by(desc(PetSupplies.regular_price)).limit(5).all()
            least_expensive_products = session.query(PetSupplies).order_by(PetSupplies.regular_price).limit(5).all()
            print("\n*** PRODUCT ANALYSIS ***")

            # Printing top-rated products
            print(Fore.RED + "\nTop rated products:" + Style.RESET_ALL)
            for product in top_rated_products:
                print(f"Name: {product.name}, Rating: {product.rating}, Num of Ratings: {product.num_ratings}, Regular Price: {product.regular_price}, Discount Price: {product.discount_price}")

            # Printing lowest-rated products
            print(Fore.RED + "\nLowest rated products:" + Style.RESET_ALL)
            for product in lowest_rating_products:
                print(f"Name: {product.name}, Rating: {product.rating}, Num of Ratings: {product.num_ratings}, Regular Price: {product.regular_price}, Discount Price: {product.discount_price}")

            # Printing most expensive products
            print(Fore.RED + "\nMost expensive products:" + Style.RESET_ALL)
            for product in most_expensive_products:
                print(f"Name: {product.name}, Rating: {product.rating}, Num of Ratings: {product.num_ratings}, Regular Price: {product.regular_price}, Discount Price: {product.discount_price}")

            # Printing least expensive products
            print(Fore.RED + "\nLeast expensive products:" + Style.RESET_ALL)
            for product in least_expensive_products:
                print(f"Name: {product.name}, Rating: {product.rating}, Num of Ratings: {product.num_ratings}, Regular Price: {product.regular_price}, Discount Price: {product.discount_price}")

            # Printing most discounted products
            print(Fore.RED + "\nMost discounted products:" + Style.RESET_ALL)
            for product in best_discount_products:
                print(
                    f"Name: {product.name}, Rating: {product.rating}, Num of Ratings: {product.product_url}, Regular Price: {product.regular_price}, Discount Price: {product.discount_price}")

        elif choice == '4':
            print('Goodbye')
            app_running = False

        else:
            print(Fore.RED + 'Invalid URL format. Please enter a valid URL.' + Style.RESET_ALL)

        if __name__ == '__main__':
            # Creating database tables
            Base.metadata.create_all(engine)
            # Adding products from CSV file to the database
            #add_csv()
            # Running the application
            app()