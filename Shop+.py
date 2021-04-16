import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from Items import Items, Inventory_Items
import os

class Interface:
    def __init__(self):
        self.selected_items = []
        self.selected_num = 0
        self.root = tk.Tk()
        self.root.title("S H O P  +")
        self.root.geometry("1080x720")
        
        # Frames to use
        self.login_frame = tk.Frame(self.root)
        self.mainScreen_frame = tk.Frame(self.root)
        self.cancelScreen_frame = tk.Frame(self.root)

        # Default packed frame
        self.login_frame.pack()
        Interface.login_credentials(self)
        self.root.mainloop()


    def login_credentials(self):
        self.username_label = tk.Label(self.login_frame, text = "Username: ")
        self.password_label = tk.Label(self.login_frame, text = "Password: ")
        self.status_button = tk.Button(self.login_frame, text = "Login", command = self.update_login)

        self.e_name = tk.Entry(self.login_frame, width = 50)
        self.e_pass = tk.Entry(self.login_frame, width = 50)

        self.username_label.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.password_label.grid(row = 1, column = 0, padx = 10, pady = 3)
        self.e_name.grid(row = 0, column = 1, padx = 10)
        self.e_pass.grid(row = 1, column = 1, padx = 10)
        self.status_button.grid(row = 3, column = 3, pady = 10)

    def update_login(self):
        if ((self.e_name.get().upper() == "CUSTOMER") and (self.e_pass.get().upper() == "PASS")):
            self.to_shopping_screen()
            self.shopping_screen()
        else:
            tk.messagebox.showerror("Error Loging in", "The entered credentials are invalid, please try again.")
            self.e_name.delete(0, tk.END)
            self.e_pass.delete(0, tk.END)

    def to_shopping_screen(self):
        self.login_frame.destroy()
        self.mainScreen_frame.pack()

    def shopping_screen(self):
        item_buttons = []
        self.button_text = []
        for i in range(len(Inventory_Items)):
            self.button_text.append(tk.StringVar())
            item_buttons.append(
                tk.Button(self.mainScreen_frame, textvariable = self.button_text[i])) # still needs to add command for executing a purchase as well as image of product

            temp_var = Items(0, Inventory_Items[i])
            self.item_name = temp_var.item_name

            self.print_info_to_button(temp_var, self.item_name, i)
            item_buttons[i].pack(side = tk.LEFT, anchor = tk.N, padx = 5, pady = 30)

    def print_info_to_button(self, product_Items, product_name, iteration):
        info_to_print = product_Items.data[product_name[iteration]]
        string_to_print = product_Items.print_inventory_data_str(info_to_print, Inventory_Items[iteration])
        self.button_text[iteration].set(string_to_print)


c = Interface()