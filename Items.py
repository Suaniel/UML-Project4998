import pandas as pd
import os


class Items:
    def __init__(self, id_num, item):
        self.item = item
        self.id_num = id_num
        self.item_name, self.item_info, self.data = Items.get_items_attributes(item)

    @staticmethod
    def get_items_attributes(item):
        baseDir = os.path.dirname(os.path.abspath(__file__))
        baseDir = baseDir + "/Inventory_item - Sheet1.csv"
        temp_data = pd.read_csv(baseDir)
        temp_itemName = list(temp_data.columns)
        temp_itemInfo = list(temp_data.index)
        return temp_itemName, temp_itemInfo, temp_data

    def print_inventory_data(self):
        for items in range(len(self.item_name)):
            print(self.item_name[items])
            temp = list(self.data[self.item_name[items]])
            print("Price: " + str(temp[0]))
            print("Availability: " + str(temp[1]))
            print()
        
    @staticmethod
    def print_inventory_data_str(product, product_name):
        string = " " + product_name
        string += "\nPrice: " + str(product[0])
        string += "\t" + "Availability: " + str(product[1])
        return string


    #def compute_purchase(self):


    #def compute_cancellation(self):
        #Function should be able to update purchases with the correct amount of balace used beforehand


Inventory_Items = ["Monster Hunter", "QANBA3", "Nintendo Switch"]


#p = Items(0, "Monster Hunter")
# p.get_items_attributes(p)
# p.print_inventory_data()

#p.print_inventory_data()

#t = p.item_name
#f = p.data[t[0]]
#value = p.print_inventory_data_str(f, Inventory_Items[0])
#print(value)