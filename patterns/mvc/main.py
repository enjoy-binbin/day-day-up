"""
(Model-View-Controller, MVC) 模型-视图-控制器模式, 这种模式用于应用程序的分层开发。

MVC模式在概念上强调 Model, View, Controller 的分离
各个模组也遵循著由 Controller 来处理讯息，Model 掌管数据来源，View 负责数据显示的职责分离的原则

核心思想是: 分层和解耦, 提高了程序的扩展性、可重用性、可维护性和可读性

模型-视图-控制器模式是应用到面向对象编程的 SoC(关注点分离)原则

是一种非常通用的设计模式，虽然我私人会认为不算是严格的设计模式，更像是一种指导架构的架构模式。

- Model(模型) 是核心的部分, 代表着应用的信息本源, 包含和管理(业务)逻辑, 数据和状态以及应用的规则.
- View(视图) 是模型的可视化表现, 它只决定怎么展示数据, 并不处理数据, 多为前端应用
- Controller(控制器) 控制器作用于模型和视图上。它控制数据流向模型对象，并在数据变化时更新视图。它使视图与模型分离开。


目前我了解到的, 基本上所有流行的Web框架例如 PHP中的 Laravel和Yii, Python中的Django
都有用到MVC或者其变种, 例如Django的MVT( Model, View, Template)
    View 视图, 和MVC里的C控制器功能相同, 接收请求, 处理业务逻辑
    Template 模板, 与MVC里的V视图功能相同, 有点不同的是返回html涉及到的模板语言会不同, 基本作用都是展示数据
    而Urlconf, 更像是控制器, 根据正则url匹配不同的视图来响应请求
"""

from models import ProductModel
from views import ProductView
from controllers import Controller

if __name__ == '__main__':
    model = ProductModel()
    view = ProductView()
    controller = Controller(model, view)

    controller.show_item_list()
    controller.show_item_info('milk')
    controller.show_item_info('apple')
