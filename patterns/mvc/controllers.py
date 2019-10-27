"""
控制器, 起到不同层面间的组织作用，用于控制应用程序的流程。

它处理事件并作出响应, 连接不同的View和Model去完成不同的需求
"""


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_item_list(self):
        item_type = self.model.item_type
        item_list = list(self.model)

        self.view.show_item_list(item_type, item_list)

    def show_item_info(self, item_name: str):
        try:
            item_info = self.model.get(item_name)
        except Exception as e:
            # print("Exception: " + str(e))
            item_type = self.model.item_type
            self.view.item_not_found(item_type, item_name)
        else:
            item_type = self.model.item_type
            self.view.show_item_info(item_type, item_name, item_info)
