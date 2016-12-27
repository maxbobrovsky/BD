import pickle

class Model:

    def __init__(self,file_name=''):
        self.__goods = []
        self.__order = []
        self.load(file_name)

    def get_goods(self):
        return self.__goods

    def get_order(self):
        return self.__order

    def load(self, file_name):
        try:
            with open(file_name,"rb") as stream:
                self.__goods, self.__order = pickle.load(stream)
        except:
            self.__goods = []
            self.__order = []

    def save (self, file_name):
        with open(file_name,"wb") as stream:
            pickle.dump([self.__goods,self.__order],stream)


    def add_goods(self,  name, category, price):
        id = 1
        if self.__goods:
            id = self.__goods[-1]['id']+1
        self.__goods.append({'id':id, 'name':name, 'category':category, 'price':price})

    def add_order(self,id_goods, number, date):
        id = 1
        if self.__order:
            id = self.__order[-1]['id']+1
        self.__order.append({'id':id, 'id_goods':id_goods, 'number':number, 'date':date})


    def del_goods(self, id):
        for x in self.__order:
            if id in x['id_goods']:
                x['id_goods']=filter(lambda s: s!=id, x['id_goods'])
                if len(x['id_goods'])==0: self.__order=filter(lambda i: i['id']!=x['id'], self.__order)
        self.__goods = filter(lambda x: x['id'] != id, self.__goods)

    def del_order(self, id,key='id'):
        self.__order = filter(lambda x: id!=x[key], self.__order)

    def update_goods(self, id, key, val):
        res = []
        for x in self.__goods:
            if x['id'] == id:
                x[key] = val
            res.append(x)
        self.__goods = res;


    def update_order(self, id, key, val):
        res = []
        for x in self.__order:
            if x['id'] == id:
                x[key] = val
            res.append(x)
        self.__order = res;

    def find (self):
        res = []
        print
        for ind in self.__goods:
            for x in self.__order:
                if ind['id'] in x['id_goods'] and ind['price']>100:
                    res.append(ind)
        print "OK"
        print res
        print "ok"
        return res

    def order_goods(self, id_goods):
        res = []
        for x in self.__order:
            if id_goods in x['id_goods']:
                res.append(x)
        return res
