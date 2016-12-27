import os

class View:

    @staticmethod
    def menu():
        print 'Menu:\n1. Order Menu\n2. Goods menu\n3. Function search\n4. Exit'

    @staticmethod
    def order_menu():
        print 'Order menu:'
        print '1. Display\n2. Add\n3. Delete\n4. Update\n5. Back'

    @staticmethod
    def goods_menu():
        print 'Goods menu:'
        print '1. Display\n2. Add\n3. Delete\n4. Update\n5. Back'

    @staticmethod
    def error_message(message):
        print 'ERROR: ' + message + '\n'

    @staticmethod
    def success_message(message):
        print message + '\n'

    @staticmethod
    def clear():
       os.system('cls')

    @staticmethod
    def display(lst):
        i = 0
        for x in lst:
            i += 1
            print  '%d) ' % i,
            for key in x:
                if key != 'id':
                    print "%+10s: %-15s" % (key, x[key]),
            print
