import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from Items import Items, Inventory_Items
import os


class Interface:
    def __init__(self):
        self.selected_items_cart = []
        self.selected_item = [0] * (len(Inventory_Items))
        self.list_of_items_purchased = []
        # self.flags = []
        self.limit_availability = []
        for i in range(len(Inventory_Items)):
            temp_var = Items(0, Inventory_Items[i])
            temp_name = temp_var.item_name
            temp = temp_var.data[temp_name[i]]
            self.limit_availability.append(temp[1])
        # self.total_price = []
        self.times_purchasing = -1
        self.root = tk.Tk()
        self.root.title("S H O P  +")
        self.root.geometry("1080x720")
        
        # Frames to use
        self.login_frame = tk.Frame(self.root)
        self.mainScreen_frame = tk.Frame(self.root)
        self.view_product_frame = tk.Frame(self.root)
        self.purchase_screen_frame = tk.Frame(self.root)
        self.purchased_items_frame = tk.Frame(self.root)
        # self.cancelScreen_frame = tk.Frame(self.root)

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
        self.mainScreen_frame.destroy()
        self.view_product_frame.destroy()
        self.purchase_screen_frame.destroy()
        self.purchased_items_frame.destroy()

        self.mainScreen_frame = tk.Frame(self.root)
        self.view_product_frame = tk.Frame(self.root)
        self.purchase_screen_frame = tk.Frame(self.root)
        self.purchased_items_frame = tk.Frame(self.root)
        self.mainScreen_frame.pack()
    
    def to_viewing_screen(self):
        self.mainScreen_frame.pack_forget()
        self.view_product_frame.pack()

    def to_cart_options(self):
        self.mainScreen_frame.destroy()
        self.purchase_screen_frame.destroy()
        self.view_product_frame.destroy()
        self.purchased_items_frame.destroy()

        self.mainScreen_frame = tk.Frame(self.root)
        self.purchase_screen_frame = tk.Frame(self.root)
        self.view_product_frame = tk.Frame(self.root)
        self.purchased_items_frame = tk.Frame(self.root)
        self.purchase_screen_frame.pack()
    
    def to_show_purchased_items(self):
        self.view_product_frame.destroy()
        self.purchase_screen_frame.destroy()

        self.view_product_frame = tk.Frame(self.root)
        self.purchase_screen_frame = tk.Frame(self.root)
        # self.reset_values()
        self.purchased_items_frame.pack()

    def shopping_screen(self):
        self.item_buttons = []
        self.button_text = []
        for i in range(len(Inventory_Items)):
            self.button_text.append(tk.StringVar())
            self.item_buttons.append(
                tk.Button(self.mainScreen_frame, textvariable = self.button_text[i],
                            command = lambda j = i: [self.to_viewing_screen(), self.viewing_screen(j)])) # still needs to add command for executing a purchase as well as image of product

            self.order_menu = tk.Menu(self.root)
            self.root.config(menu = self.order_menu)

            cart_cancel_menu = tk.Menu(self.order_menu)
            self.order_menu.add_cascade(label = "Orders", menu = cart_cancel_menu)
            cart_cancel_menu.add_command(label = "Go to Cart", command = lambda: [self.to_cart_options(), self.cart_options()])
            cart_cancel_menu.add_command(label = "Main Screen", command = lambda: [self.to_shopping_screen(), self.shopping_screen()])
            cart_cancel_menu.add_separator()
            cart_cancel_menu.add_command(label = "Log Out", command = self.root.quit)

            temp_var = Items(0, Inventory_Items[i])
            self.item_name = temp_var.item_name

            self.print_info_to_button(temp_var, self.item_name, i)
            self.item_buttons[i].pack(side = tk.LEFT, anchor = tk.N, padx = 5, pady = 30)
    
    def viewing_screen(self, to_view):
        selected_item = Items(0, Inventory_Items[to_view])
        item_name_label = selected_item.item_name
        label_text = tk.StringVar()
        showing_item = tk.Label(self.view_product_frame, textvariable = label_text)
        self.print_info_to_label(selected_item, item_name_label, label_text, to_view)

        self.spinbox = tk.Spinbox(self.view_product_frame, from_ = 0, to = self.limit_availability[to_view])
        cart_button = tk.Button(self.view_product_frame, text = "Add to Cart", command = lambda: [self.update_selection(to_view), self.to_shopping_screen(), self.shopping_screen()])
        if ((self.limit_availability[to_view] == 0)):
            cart_button['state'] = tk.DISABLED
        back_button = tk.Button(self.view_product_frame, text = "Back", command = lambda: [self.to_shopping_screen(), self.shopping_screen()])

        showing_item.pack(side = tk.TOP, anchor = tk.N, pady = 30)
        back_button.pack(side = tk.RIGHT, anchor = tk.E, padx = 15, pady = 15)
        cart_button.pack(side = tk.RIGHT, anchor = tk.E, padx = 15)
        self.spinbox.pack(side = tk.RIGHT, anchor = tk.E, padx = 30)

    def cart_options(self):
        self.item_labels = []
        amount_to_pack = -1
        item_text = []
        tax_rate = .115
        gross_price = 0.00
        total_price = 0
        flag_showPrice = False
        for i in range(len(Inventory_Items)):
            if (self.selected_item[i] > 0):
                flag_showPrice = True
                item_text = tk.StringVar()
                self.item_labels.append(
                    tk.Label(self.purchase_screen_frame, textvariable = item_text))

                temp_var = Items(0, Inventory_Items[i])
                gross_price += Items.compute_total(temp_var, i) * (float(self.selected_item[i]))
                self.list_of_items_purchased.append((temp_var.item_name[i], self.selected_item[i])) #bring price OR pass it by reference in the function self.show_purchased_items()

                amount_to_pack += 1
                self.print_info_to_label(temp_var, temp_var.item_name, item_text, i)
                self.item_labels[amount_to_pack].pack(side = tk.RIGHT, anchor = tk.E, padx = 30, pady = 30)
        total_price = (gross_price * tax_rate) + gross_price
        print(self.list_of_items_purchased)
        print(self.selected_item)
        if (flag_showPrice == True):
            to_pay = tk.Label(self.purchase_screen_frame, text = "TOTAL: " + str(total_price))
            purchase_button = tk.Button(self.purchase_screen_frame, text = "PLACE ORDERS", bg = '#90ee90', 
                                        command = lambda: [self.increment_times_purchased(), self.reset_values(), self.to_show_purchased_items(), self.show_purchased_items()])
            cancel_button = tk.Button(self.purchase_screen_frame, text = "Cancel Orders", bg = '#FF7276')
            to_pay.pack(side = tk.BOTTOM, anchor = tk.W, padx = 50, pady = 40)
            purchase_button.pack()
            cancel_button.pack()

        else:
            message_label = tk.Label(self.purchase_screen_frame, text = "No Items have been added to Cart")
            message_label.pack(side = tk.BOTTOM, anchor = tk.W, padx = 50, pady = 40)

    def show_purchased_items(self):
        self.p_items_labels = []
        p_items_text = []
        check_itr = 0
        for i in range(len(self.list_of_items_purchased)):
            p_items_text = tk.StringVar()
            self.p_items_labels.append(
                tk.Label(self.purchased_items_frame, textvariable = p_items_text))
            check_itr = Items.print_price_purchase(self.list_of_items_purchased[i][0])
            self.print_purchased_info(self.list_of_items_purchased[i][0], self.list_of_items_purchased[i][1], p_items_text, i, check_itr)
            self.p_items_labels[i].pack(side = tk.RIGHT, padx = 15, pady = 30)
        

    # In order printing to labels and Buttons
    def print_info_to_button(self, product_Items, product_name, iteration):
        info_to_print = product_Items.data[product_name[iteration]]
        string_to_print = product_Items.print_inventory_data_str(info_to_print, Inventory_Items[iteration])
        string_to_print += "\t" + "Original Availability: " + str(self.limit_availability[iteration])
        self.button_text[iteration].set(string_to_print)

    def print_info_to_label(self, product_Items, product_name, label, iteration):
        info_to_print = product_Items.data[product_name[iteration]]
        string_to_print = product_Items.print_inventory_data_str(info_to_print, Inventory_Items[iteration])
        string_to_print += "\t" + "Current Availability: " + str(self.limit_availability[iteration])
        label.set(string_to_print)
    
    def print_purchased_info(self, product_name, amount, label, iterator, aux_itr): # EDIT
        product_Items = Items(0, Inventory_Items[aux_itr])
        info_to_print = product_Items.data[product_name]
        string_to_print = "Purchase #" + str(self.times_purchasing) + "\n\n"
        string_to_print = product_Items.print_inventory_data_str(info_to_print, product_name)
        string_to_print += "\t" + "Amount purchased: " + str(amount)
        #if (self.flags[iterator + 1] == True):
        #    string_to_print += "\n" + "Total for purchase #" + str(iterator + 1) + ":\t" + str(self.total_price[self.times_purchasing])
        # print(self.total_price)
        print(self.times_purchasing)
        # print(self.total_price[self.times_purchasing])
        print(string_to_print)
        label.set(string_to_print)

    def update_selection(self, item_id):
        self.selected_item[item_id] += int(self.spinbox.get())
        self.limit_availability[item_id] -= int(self.spinbox.get())
    
    def increment_times_purchased(self):
        self.times_purchasing += 1
        # self.flags.append(True)
        print(self.times_purchasing)
        # print(self.flags)

    def reset_values(self):
        self.selected_item = [0] * len(Inventory_Items)


c = Interface()