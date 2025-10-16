# 导出所有模型
from app.models.user import User
from app.models.role import Role
from app.models.customer import Terminal, DirectDistributor, KOL, CustomerContact
from app.models.visit import VisitPlan, VisitRoute, VisitRecord
from app.models.order import SalesOrder, ReturnOrder, DeliveryOrder
from app.models.product import Product
from app.models.inventory import Inventory

__all__ = [
    'User', 'Role',
    'Terminal', 'DirectDistributor', 'KOL', 'CustomerContact',
    'VisitPlan', 'VisitRoute', 'VisitRecord',
    'SalesOrder', 'ReturnOrder', 'DeliveryOrder',
    'Product', 'Inventory'
]

