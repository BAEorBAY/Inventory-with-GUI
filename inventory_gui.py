import tkinter as tk
import os
class Item:
    def __init__(self, name, price, quantity, category):
        self.name = name
        self.price = float(price)
        self.quantity = int(quantity)
        self.category = category  # Assuming category is the first word of the name

    def __str__(self):
        return f"{self.name} |   ${self.price:.2f} |  {self.quantity} pcs | {self.category}"
    
class Inventory:
    def __init__(self):
        self.store = []

    def add_item(self, item):
        self.store.append(item)

    def get_all_items(self):
        return self.store

inventory = Inventory()    


window = tk.Tk()
window.title("Inventory Manager")
window.geometry("400x500")

# Name
name_label = tk.Label(window, text="Item Name:")
name_label.pack()
name_entry = tk.Entry(window)
name_entry.pack()

# Price
price_label = tk.Label(window, text="Price:")
price_label.pack()
price_entry = tk.Entry(window)
price_entry.pack()

#Quantity
quantity_label = tk.Label(window, text="Quantity:")
quantity_label.pack()
quantity_entry = tk.Entry(window)
quantity_entry.pack()

# Category
category_label = tk.Label(window, text="Category:")
category_label.pack()
category_entry = tk.Entry(window)
category_entry.pack()



category_options = ["All", "Fruits", "Drinks", "Utensils", "stationary"]  # You can update this list as you go
selected_category = tk.StringVar()
selected_category.set("All")

def on_category_change(*args):
    selected = selected_category.get()
    if selected == "All":
        inventory_listbox.delete(0, tk.END)  # Clear the listbox
        for item in inventory.get_all_items():
            inventory_listbox.insert(tk.END, str(item))
    else:
        filter_by_category(selected)        

# == Search Find ===

search_label = tk.Label(window, text="Search Item:")
search_label.pack()
search_entry = tk.Entry(window)
search_entry.pack()  

# == Add Buttons ===
def add_item():
    name = name_entry.get()
    price = price_entry.get()
    quantity = quantity_entry.get()
    category = category_entry.get()  # Get the category from the entry field
    
    if name and price and quantity and category:
        try:
           item = Item(name, float(price), int(quantity), category)
           inventory.add_item(item)
           inventory_listbox.insert(tk.END, str(item))  # Clear the listbox
           #clear the input fields
           name_entry.delete(0, tk.END)
           price_entry.delete(0, tk.END)
           quantity_entry.delete(0, tk.END)
           category_entry.delete(0, tk.END)
        except ValueError:
            print("Invalid input. Please enter valid price and quantity.")      
    else:
        print("Please fill in all fields.")

def filter_by_category(category):
    inventory_listbox.delete(0, tk.END)
    for item in inventory.get_all_items():
        if item.category.lower() == category.lower():
            inventory_listbox.insert(tk.END, str(item))
       
def delete_item():
    selected_index = inventory_listbox.curselection()
    if selected_index:
        inventory_listbox.delete(selected_index)
        # Remove from inventory as well
        del inventory.store[selected_index[0]]
    else:
        print("No item selected to delete.")      

def save_inventory_by_category():
    os.makedirs("InventoryFiles", exist_ok=True)  # Create directory if it doesn't exist
    
    for item in inventory.get_all_items():
        filename = f"InventoryFiles/{item.category}.txt"
        with open(filename, "w") as file:
            file.write(f"{item.name},{item.price},{item.quantity},{item.category}\n")
            
        print(f"Item '{item.name}' saved to {filename}")    

def load_all_category_files():
    inventory.store.clear()  # Clear current inventory
    inventory_listbox.delete(0, tk.END)  # Clear the listbox
    
    folder = "InventoryFiles"
    if not os.path.exists(folder):
        print("No inventory files found.")
        return
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            with open(os.path.join(folder, filename), "r") as file:
                for line in file:
                    name, price, quantity, category = line.strip().split(',')
                    item = Item(name, float(price), int(quantity), category)
                    inventory.add_item(item)
                    inventory_listbox.insert(tk.END, str(item))

def search_item():
    query = search_entry.get().lower()
    inventory_listbox.selection_clear(0, tk.END)  # Clear previous selections  
    
    found = False
    for i, item in enumerate(inventory.get_all_items()):
        if query in item.name.lower():
            inventory_listbox.selection_set(i)
            inventory_listbox.see(i)
            found = True
    if not found:
        print(f"No item found matching '{query}'.")     
      



search_button = tk.Button(window, text="Search", command=search_item)
search_button.pack(pady=10)

filter_label = tk.Label(window, text="Filter by Category:")
filter_label.pack()
category_dropdown = tk.OptionMenu(window, selected_category, *category_options, command=lambda _: on_category_change())
category_dropdown.pack(pady=5) 
                        
add_button = tk.Button(window, text="Add Item", command=add_item)
add_button.pack(pady=10)

save_button = tk.Button(window, text="Save by category", command=save_inventory_by_category)
save_button.pack(pady=5)

load_button = tk.Button(window, text="Load all category", command=load_all_category_files)
load_button.pack(pady=5)

delete_button = tk.Button(window, text="Delete Item", command=delete_item)
delete_button.pack(pady=10)


# ===== LISTBOX TO SHOW INVENTORY =====
inventory_listbox = tk.Listbox(window, width=50)
inventory_listbox.pack(pady=10)

window.mainloop()