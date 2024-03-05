import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import spacy
import json

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Load mock database from JSON file
with open("C:/Users/Charvi Jain/Desktop/ds_assessment/mock_db.json", "r") as file:
    mock_db = json.load(file)

class SearchProductWindow:
    def __init__(self, master, info_callback):
        self.master = master
        master.title("Search Products")
        self.info_callback = info_callback  # Callback function to open information window

        self.label = tk.Label(master, text="Enter product name to search:", font=("Arial", 14))
        self.label.pack()

        self.search_entry = tk.Entry(master, font=("Arial", 12))
        self.search_entry.pack()

        self.search_button = tk.Button(master, text="Search", command=self.search_product, font=("Arial", 12), bg="blue", fg="white")
        self.search_button.pack()

        # Create a frame to hold the treeview and scrollbar
        self.tree_frame = tk.Frame(master)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        # Create horizontal scrollbar
        self.scrollbar_x = tk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Create treeview with horizontal scrolling
        self.tree = ttk.Treeview(self.tree_frame, columns=('Name', 'Price', 'Description'), show='headings', xscrollcommand=self.scrollbar_x.set)
        self.tree.heading('Name', text='Name')
        self.tree.heading('Price', text='Price')
        self.tree.heading('Description', text='Description')

        # Attach scrollbar to treeview
        self.scrollbar_x.config(command=self.tree.xview)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree.bind("<Double-1>", self.on_double_click)  # Bind double-click event to treeview

    def search_product(self):
        search_query = self.search_entry.get().strip().lower()
        if not search_query:
            messagebox.showwarning("Warning", "Please enter a product name to search.")
            return

        self.tree.delete(*self.tree.get_children())
        for product in mock_db['products']:
            if search_query in product['name'].lower():
                self.tree.insert('', 'end', values=(product['name'], product['price'], product['description']))

    def on_double_click(self, event):
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, 'values')
        if values:
            product_name, _, product_description = values
            self.info_callback(product_name, product_description)


class InformationWindow:
    def __init__(self, master, product_name, product_description):
        self.master = master
        master.title("Product Information")

        self.label = tk.Label(master, text="Product Information", font=("Arial", 16))
        self.label.pack()

        self.product_name_label = tk.Label(master, text=f"Product: {product_name}", font=("Arial", 12))
        self.product_name_label.pack()

        self.product_description_label = tk.Label(master, text=f"Description: {product_description}", font=("Arial", 12))
        self.product_description_label.pack()

        self.reviews_label = tk.Label(master, text="Reviews:", font=("Arial", 12))
        self.reviews_label.pack()

        # Create a frame to hold the reviews
        self.reviews_frame = tk.Frame(master)
        self.reviews_frame.pack()

        # Display reviews
        self.display_reviews(product_name)

    def display_reviews(self, product_name):
        for product in mock_db['products']:
            if product['name'] == product_name and 'reviews' in product:
                for review in product['reviews']:
                    review_text = f"Rating: {review['rating']}, Description: {review['description']}"
                    review_label = tk.Label(self.reviews_frame, text=review_text, font=("Arial", 10), wraplength=400, justify=tk.LEFT)
                    review_label.pack(anchor=tk.W)



class ReviewWindow:
    def __init__(self, master):
        self.master = master
        master.title("Add Review")

        self.label = tk.Label(master, text="Add Review", font=("Arial", 16))
        self.label.pack()

        self.product_var = tk.StringVar(master)
        self.product_var.set("Select Product")
        self.product_menu = ttk.Combobox(master, textvariable=self.product_var)
        self.product_menu['values'] = [product['name'] for product in mock_db['products']]
        self.product_menu.pack()

        self.rating_label = tk.Label(master, text="Rating:", font=("Arial", 12))
        self.rating_label.pack()
        self.rating_entry = ttk.Combobox(master, values=[0, 1, 2, 3, 4, 5], font=("Arial", 12))
        self.rating_entry.pack()

        self.desc_label = tk.Label(master, text="Description:", font=("Arial", 12))
        self.desc_label.pack()
        self.desc_entry = tk.Entry(master, font=("Arial", 12))
        self.desc_entry.pack()

        self.add_button = tk.Button(master, text="Add Review", command=self.add_review, font=("Arial", 12), bg="blue", fg="white")
        self.add_button.pack()

    def add_review(self):
        product_name = self.product_var.get()
        rating = self.rating_entry.get()
        description = self.desc_entry.get()

        if not product_name or not rating or not description:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        for product in mock_db['products']:
            if product['name'] == product_name:
                product['reviews'].append({'rating': int(rating), 'description': description})
                messagebox.showinfo("Success", "Review added successfully.")
                break


class SpaCyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Ecommerce Catalog")
        master.geometry("400x300")  # Set initial window size

        self.label = tk.Label(master, text="Choose an action you want to perform:", font=("Arial", 14))
        self.label.pack()

        self.button_search = tk.Button(master, text="Search Products", command=self.open_search_window, font=("Arial", 12), bg="green", fg="white")
        self.button_search.pack(pady=10)

        self.button_add_review = tk.Button(master, text="Add Review", command=self.open_review_window, font=("Arial", 12), bg="orange", fg="white")
        self.button_add_review.pack(pady=10)

        self.button_status = tk.Button(master, text="Check Status", command=self.check_status, font=("Arial", 12), bg="red", fg="white")
        self.button_status.pack(pady=10)

    def open_search_window(self):
        self.master.withdraw()
        search_window = tk.Toplevel(self.master)
        search_window.title("Search Products")
        search_window.geometry("600x400")  # Set window size
        search_window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(search_window))

        # Create the search product window
        search_app = SearchProductWindow(search_window, self.open_info_window)

    def open_info_window(self, product_name, product_description):
        info_window = tk.Toplevel(self.master)
        info_window.title("Product Information")
        info_window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(info_window))

        # Create the information window
        info_app = InformationWindow(info_window, product_name, product_description)

    def open_review_window(self):
        review_window = tk.Toplevel(self.master)
        review_window.title("Add Review")
        review_window.protocol("WM_DELETE_WINDOW", lambda: self.close_window(review_window))

        # Create the review window
        review_app = ReviewWindow(review_window)

    def close_window(self, window):
        window.destroy()
        self.master.deiconify()

    def check_status(self):
        messagebox.showinfo("Status", "Our services are currently operational.\nThank you for your interest!")


root = tk.Tk()
app = SpaCyGUI(root)
root.mainloop()
