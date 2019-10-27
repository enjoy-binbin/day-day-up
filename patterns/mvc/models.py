"""
模型Model, 核心最重要的部分, 是对客观事物的抽象, 一般来说也是最复杂的
包含检验、业务处理、访问应用数据(数据库表等)
三个模块保持相互独立, Model可以方便的改变程序的数据层和业务规则, 例如数据库移植
"""


class ModelBase(type):
    def __new__(cls, name, bases, attrs, **kwargs):

        attr_meta = attrs.pop('Meta', None)
        abstract = getattr(attr_meta, 'abstract', False)
        if abstract:
            print('Abstract Model')
        else:
            print('Normal Model')
        print('')

        return super().__new__(cls, name, bases, attrs)


class Model(metaclass=ModelBase):
    @property
    def item_type(self):
        raise NotImplementedError

    def get(self, item: str):
        raise NotImplementedError

    def save(self):
        pass

    def __iter__(self):
        raise NotImplementedError

    class Meta:
        abstract = True


class ProductModel(Model):
    class Price(float):
        def __str__(self):
            return "{:.2f}".format(self)

    item_type = 'product'
    products = {
        'banana': {
            'verbose_name': '香蕉', 'price': Price(1.50), 'quantity': 10
        },
        'milk': {
            'verbose_name': '牛奶', 'price': Price(3.50), 'quantity': 25
        },
        'ice_cream': {
            'verbose_name': '冰淇淋', 'price': Price(6.00), 'quantity': 10
        },
    }

    def get(self, product: str):
        try:
            return self.products[product]
        except KeyError as e:
            raise KeyError((str(e) + " not in the product list."))

    def __iter__(self):
        for product in self.products:
            yield product
