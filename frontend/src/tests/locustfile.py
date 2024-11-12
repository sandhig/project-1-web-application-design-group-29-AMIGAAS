from locust import HttpUser, task, between
import os

# Shared storage for authentication data
auth_data = {"token": None}
test_image_path = os.path.join(os.path.dirname(__file__), 'table.jpg')

# Backend user logs in and stores the token
class TestUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Authenticate and get a token for future requests
        self.login()

    # Login as a authenticated user for rest of the tests
    def login(self):
        login_url = "/profiles/login"
        response = self.client.post(login_url, json={"email": "test@mail.utoronto.ca", "password": "123"})
        if response.status_code == 200:
            # Extract and store token or session cookie
            auth_data["token"] = response.json().get("token")
        else:
            print("Login failed. Please check credentials.")
    
    @task(1)
    # login as a user, don't use this for anything else
    def login_user(self):
        login_url = "/profiles/login"
        response = self.client.post(login_url, json={"email": "test@mail.utoronto.ca", "password": "123"})
        if response.status_code == 200:
            print("Login successful, token stored.")
        else:
            print("Login failed.")

    # View products homepage
    @task(2)
    def product_homepage(self):
        product_homepage_url = "/products"
        headers = {"Authorization": f"Token {auth_data['token']}"}
        response = self.client.get(product_homepage_url, headers=headers)
        if response.status_code == 200:
            print("Retrieved product homepage successfully")
        else:
            print(f"Failed to retrieve products. Status: {response.status_code}")

    
    @task(3)
    # View profile
    def view_profile(self):
        user_id = 2
        user_profile_url = f"/user/{user_id}"
        headers = {"Authorization": f"Token {auth_data['token']}"}
        response = self.client.get(user_profile_url, headers=headers)
        if response.status_code == 200:
            print("Retrieved user profile successfully")
        else:
            print(f"Failed to retrieve user profile. Status: {response.status_code}")

    
    @task(4)
    # View wishlist
    def view_wishlist(self):
        wishlist_url = "/wishlist"
        headers = {"Authorization": f"Token {auth_data['token']}"}
        response = self.client.get(wishlist_url, headers=headers)
        if response.status_code == 200:
            print("Retrieved user's wishlist successfully")
        else:
            print(f"Failed to retrieve user's wishlist. Status: {response.status_code}")

    
    @task(5)
    # View a single product listing
    def view_single_product(self):
        pk = 57
        product_detail_url = f"/products/{pk}"
        headers = {"Authorization": f"Token {auth_data['token']}"}
        response = self.client.get(product_detail_url, headers=headers)
        if response.status_code == 200:
            print("Retrieved product detail successfully")
        else:
            print(f"Failed to retrieve product detail. Status: {response.status_code}")
    

    @task(6)
    # Create a listing
    def create_product(self):
        data = {
            "name": "Locust Test Product",
            "category": "Furniture",
            "price": "175.00",
            "condition": "Good",
            "pickup_location": "Bahen",
            "description": "This is a test product for load testing"
        }
        headers = {"Authorization": f"Token {auth_data['token']}"}
        files = {
            "image": open(test_image_path, "rb")  # Provide an actual file path for uploading an image
        }
        response = self.client.post("/products/", headers=headers, data=data, files=files)
        
        if response.status_code == 201:
            print("Product created successfully.")
        else:
            print(f"Failed to create product. Status: {response.status_code}")

    

# # Define tasks for frontend (GET only)
# class FrontEndUser(HttpUser):
#     # Set the frontend host (aws amazon URL)
#     host = "http://toogoodtothrow.s3-website.us-east-2.amazonaws.com/"
#     wait_time = between(1, 3)

#     # Visit welcome page
#     @task(1)
#     def load_homepage(self):
#         self.client.get("/")
#         print("Homepage loaded successfully")
    

    # # Visit the Ho
    # @task(3)
    # def category_textbook(self):
    #     response = self.client.get("/category?query=textbook")
    #     if response.status_code == 200:
    #         print("Navigate to category successful!")
    #     else:
    #         print("Navigate to category failed.")

    # # Visit my profile
    # @task(2)
    # def view_profile(self):
    #     if auth_data["token"]:
    #         user_id = 2
    #         headers = {"Authorization": f"Bearer {auth_data['token']}"}
    #         response = self.client.get(f"/user/{user_id}", headers=headers)
            
    #         # if response.status_code == 200:
    #         #     print("Profile accessed successfully!")
    #         # else:
    #         #     print("Failed to access profile.")
    #         if response.status_code == 200:
    #             print("Profile accessed successfully!")
    #             print("Profile data:", response.json())  # Optionally log profile data
    #         else:
    #             print(f"Failed to access profile. Status code: {response.status_code}")
    #     else:
    #         print("No token available for authenticated request.")

    
    
    
    # # Carry out a search
    # @task(4)
    # def search(self):
    #     search_term = "Test"  # Replace with a term or set dynamically
    #     response = self.client.get(f"/search?query={search_term}")
    #     if response.status_code == 200:
    #         print("Search successful!")
    #     else:
    #         print("Search failed.")

    
    # Check out wishlist - GET
    # check out create listing - POST
    # 