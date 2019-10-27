"""
视图View, 实现数据有目的的显示, 理论上不是必需的

同一个Model可以被不同的View重用(pc, h5..), 提高了代码的可重用性
"""
from mixins import StringMixin


class View:
    def show_item_list(self, item_type: str, item_list: list):
        raise NotImplementedError

    def show_item_info(self, item_type: str, item_name: str, item_info: dict):
        raise NotImplementedError

    def item_not_found(self, item_type: str, item_name: str):
        raise NotImplementedError


class ProductView(View, StringMixin):
    def show_item_list(self, item_type: str, item_list: list):
        print(item_type + ' 列表:')
        print(', '.join(item_list))
        print('')

    def show_item_info(self, item_type: str, item_name: str, item_info: dict):
        print(self.capitalize(item_type) + ' info:')
        printout = 'Name: %s' % item_name
        for key, value in item_info.items():
            printout += ', ' + self.capitalize(key) + ': ' + str(value)  # __str__
        printout += '\n'
        print(printout)

    def item_not_found(self, item_type: str, item_name: str):
        print('That %s "%s" does not exist in the records' % (item_type, item_name))
