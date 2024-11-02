import tkinter as tk
from tkinter import ttk

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def custom_hash_function(self, key):
        # Custom hash function: Sum of digits
        return sum(int(digit) for digit in str(key)) % self.size

    def linear_probe(self, index):
        initial_index = index
        while self.table[index] is not None:
            index = (index + 1) % self.size
            if index == initial_index:
                return None  # No empty slot found, the table is full
        return index

    def double_hash_probe(self, key, iteration):
        hash_prime = 7  # Choose a prime number as the hash prime
        return (self.custom_hash_function(key) + iteration * hash_prime) % self.size

    def find_index(self, key, method):
        if method == "linear":
            index = self.custom_hash_function(key)
            initial_index = index
            while self.table[index] is not None:
                if self.table[index][0] == key:
                    return index
                index = (index + 1) % self.size
                if index == initial_index:
                    return None  # Key not found and table is full
            return index
        elif method == "double":
            index = self.custom_hash_function(key)
            iteration = 0
            while True:
                new_index = self.double_hash_probe(key, iteration)
                if self.table[new_index] is None or self.table[new_index][0] == key:
                    return new_index
                iteration += 1

    def delete(self, key, method):
        index = self.find_index(key, method)
        if index is None:
            raise Exception("Key not found in the hash table.")
        # Delete the key
        deleted_item = self.table[index]
        self.table[index] = None
        print(f"Deleted item: {deleted_item}")
        # Reorganize the table to maintain coherence
        current_index = index
        next_index = (current_index + 1) % self.size
        while self.table[next_index] is not None:
            next_hash = self.custom_hash_function(self.table[next_index][0])
            if (method == "linear" and next_hash <= current_index) or (
                method == "double" and next_hash < current_index
            ):
                self.table[current_index] = self.table[next_index]
                self.table[next_index] = None
                current_index = next_index
            next_index = (next_index + 1) % self.size

    def insert(self, key, value, method):
        index = self.find_index(key, method)
        if index is None:
            raise Exception("Hash table full, unable to insert element.")
        self.table[index] = (key, value)

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Hash Table")
        self.hash_table = HashTable(10)  # Choose the hash table size here
        self.label = ttk.Label(master, text="Key:")
        self.label.grid(row=0, column=0)
        self.key_entry = ttk.Entry(master)
        self.key_entry.grid(row=0, column=1)
        self.label = ttk.Label(master, text="Value:")
        self.label.grid(row=1, column=0)
        self.value_entry = ttk.Entry(master)
        self.value_entry.grid(row=1, column=1)
        self.method_label = ttk.Label(master, text="Collision Resolution Method:")
        self.method_label.grid(row=2, column=0)
        self.method_var = tk.StringVar()
        self.method_var.set("linear")  # Default choice
        self.method_dropdown = ttk.OptionMenu(master, self.method_var, "linear", "linear", "double")
        self.method_dropdown.grid(row=2, column=1)
        self.insert_button = ttk.Button(master, text="Insert", command=self.insert)
        self.insert_button.grid(row=3, column=0, columnspan=2)
        self.delete_button = ttk.Button(master, text="Delete", command=self.delete)
        self.delete_button.grid(row=4, column=0, columnspan=2)
        self.lookup_button = ttk.Button(master, text="Lookup", command=self.lookup)
        self.lookup_button.grid(row=5, column=0, columnspan=2)
        self.result_label = ttk.Label(master, text="")
        self.result_label.grid(row=6, column=0, columnspan=2)
        self.tree = ttk.Treeview(master, columns=('Index', 'Key', 'Value'), show='headings')
        self.tree.heading('Index', text='Index')
        self.tree.heading('Key', text='Key')
        self.tree.heading('Value', text='Value')
        self.tree.grid(row=7, column=0, columnspan=2)

    def lookup(self):
        key = int(self.key_entry.get())
        method = self.method_var.get()
        try:
            index = self.hash_table.find_index(key, method)
            if index is not None:
                self.result_label.config(text=f"Key {key} found at index {index}.")
            else:
                self.result_label.config(text=f"Key {key} not found in the hash table.")
        except Exception as e:
            self.result_label.config(text=str(e))

    def insert(self):
        key = int(self.key_entry.get())
        value = self.value_entry.get()
        method = self.method_var.get()
        try:
            self.hash_table.insert(key, value, method)
            self.result_label.config(text="Insertion successful.")
            self.update_tree()
            # Clear the entry fields after successful insertion
            self.key_entry.delete(0, tk.END)
            self.value_entry.delete(0, tk.END)
        except Exception as e:
            self.result_label.config(text=str(e))

    def delete(self):
        key = int(self.key_entry.get())
        method = self.method_var.get()
        try:
            self.hash_table.delete(key, method)
            self.update_tree()
            # Clear the entry fields after successful deletion
            self.key_entry.delete(0, tk.END)
            self.value_entry.delete(0, tk.END)
        except Exception as e:
            self.result_label.config(text=str(e))

    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        for index, item in enumerate(self.hash_table.table):
            if item is not None:
                self.tree.insert('', 'end', values=(index, item[0], item[1]))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()