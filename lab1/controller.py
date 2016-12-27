from model import Model
from view import View

class Controller:

    def __init__(self,f_name):
        self.file_name = f_name
        self.dbase = Model(f_name)

    def menu(self):
        choice = -1
        while choice != 4:
            View.clear()
            View.menu()
            try:
                choice = int (raw_input('Enter menu item:\n'))
            except  ValueError:
                View.error_message('Incorrect value')

            if choice == 1:
                self.order_menu()

            elif choice == 2:
                self.goods_menu()

            elif choice == 3:
                View.clear()
                print '\tGoods cost less than 100 hrn:'
                res = self.dbase.find()
                View.display(res)
                print '0)   Back'
                item = -1
                while item < 0 or item > len (res):
                    try:
                        item = int(raw_input('Enter number item:\n'))
                    except ValueError:
                        View.error_message('Incorrect value')
                if item != 0:
                    View.clear()
                    View.display(self.dbase.order_goods((res[item-1]['id'])))
                    raw_input('Press Enter to continue...')

            elif choice == 4:
                self.dbase.save(self.file_name)
        View.clear()

    def order_menu(self):
        choice = -1
        while choice != 5:
            View.clear()
            View.order_menu()
            try:
                choice = int(raw_input('Enter menu item:\n'))
            except ValueError:
                View.error_message('Incorrect value')

            if choice == 1:
                View.clear()
                View.display(self.dbase.get_order())
                print
                raw_input("Press any key to continue...")


            elif choice == 2:
                View.clear()
                View.display( self.dbase.get_goods())
                a = []
                b = []
                ans = -1
                while ans < 0:
                    id_goods = -1
                    while id_goods < 1 or id_goods > len(self.dbase.get_goods()):
                        try:
                            id_goods = int(raw_input('Enter acticle goods:\n'))
                        except ValueError:
                            View.error_message('Incorrect value')
                    a.append(id_goods)

                    number = -1
                    while number < 1:
                        try:
                            number = int(raw_input('Enter number goods:\n'))
                        except ValueError:
                            View.error_message('Incorrect value')
                    b.append(number)

                    i = -1
                    while i != 1 and i != 0:
                        try:
                            i = int(raw_input("Add more press [1], else press [0]?\n"))
                        except ValueError:
                            View.error_message('Incorrect value')
                        if i == 1:
                            ans = -1
                        else:
                            ans = 1


                date = raw_input('Enter the date order:\n')
                self.dbase.add_order(a,b,date)

            elif choice == 3 or choice == 4:
                View.clear()
                View.display(self.dbase.get_order())
                print '0)   Back'
                item = -1
                while item != 0:
                    try:
                        item = int(raw_input('\nEnter number item:\n'))
                    except ValueError:
                        View.error_message('Incorrect vaue')

                    if item > 0 and item <= len(self.dbase.get_order()):
                        id = self.dbase.get_order()
                        id = id[item-1]['id']
                        if choice == 3:
                            self.dbase.del_order(id)
                            View.success_message('Item deleted!')
                        else:
                            key =raw_input(('\nEnter title attr:\n'))
                            while not(key in ['id_goods','number','date']):
                                View.error_message('Incorrect key attr')
                                key = raw_input('\nEnter title attr:\n')
                            if key == 'id_goods' or key == 'number':
                                a = []
                                b = []
                                ans = -1
                                while ans < 0:
                                    id_goods = -1
                                    while id_goods < 1 or id_goods > len(self.dbase.get_goods()):
                                        try:
                                            id_goods = int(raw_input('Enter acticle goods:\n'))
                                        except ValueError:
                                            View.error_message('Incorrect value')
                                    a.append(id_goods)

                                    number = -1
                                    while number < 1:
                                        try:
                                            number = int(raw_input('Enter number goods:\n'))
                                        except ValueError:
                                            View.error_message('Incorrect value')
                                    b.append(number)

                                    i = -1
                                    while i != 1 and i != 0:
                                        try:
                                            i = int(raw_input("Add more press [1], else press [0]?\n"))
                                        except ValueError:
                                            View.error_message('Incorrect value')
                                        if i == 1:
                                            ans = -1
                                        else:
                                            ans = 1
                                self.dbase.update_order(id, 'id_goods', a)
                                self.dbase.update_order(id,'number',b)
                            else:
                                val = raw_input('Enter value attr:\n')
                                self.dbase.update_order(id,key,val)
                            View.success_message('Item update!')
                        item = 0

    def goods_menu(self):
        choice = -1
        while choice != 5:
            View.clear()
            View.goods_menu()
            try:
                choice = int(raw_input('Enter menu item:\n'))
            except ValueError:
                View.error_message('Incorrect value')

            if choice == 1:
                View.clear()
                View.display(self.dbase.get_goods())
                raw_input('Press Enter to continue...')

            elif choice == 2:
                View.clear()
                name = raw_input('Enter name goods:\n')
                category = raw_input('Enter category goods:\n')
                price = int(raw_input('Enter price goods:\n'))
                self.dbase.add_goods(name,category,price)

            elif choice == 3 or choice == 4:
                View.clear()
                View.display(self.dbase.get_goods())
                print '0)   Back'
                item = -1
                while item != 0:
                    try:
                        item = int (raw_input('\nEnter number item:\n'))
                    except ValueError:
                        View.error_message('Incorrect value')

                    if item > 0 and item <= len (self.dbase.get_goods()):
                        id = self.dbase.get_goods()
                        id = id[item-1]['id']
                        if choice == 3:
                            self.dbase.del_goods(item)
                            View.success_message('Item deleted!')
                        else:
                            key = raw_input('\nEnter title attr:\n')
                            while not (key in ['name','category','price']):
                                View.error_message('Inccorrect key attr')
                                key = raw_input('\nEnter title attr:\n')
                            val = raw_input('Enter value attr:\n')
                            self.dbase.update_goods(id,key,val)
                            View.success_message('Item update!')
                        item = 0

