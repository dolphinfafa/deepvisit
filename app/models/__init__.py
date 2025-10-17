# 导出所有模型
from app.models.user import User
from app.models.role import Role
from app.models.customer import Terminal, DirectDistributor, KOL, CustomerContact
from app.models.visit import VisitPlan, VisitRoute, VisitRecord
from app.models.order import SalesOrder, ReturnOrder, DeliveryOrder
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.supplier import Supplier
from app.models.warehouse import Warehouse
from app.models.purchase_order import PurchaseOrder
from app.models.activity import Activity, ActivityReport

__all__ = [
    'User', 'Role',
    'Terminal', 'DirectDistributor', 'KOL', 'CustomerContact',
    'VisitPlan', 'VisitRoute', 'VisitRecord',
    'SalesOrder', 'ReturnOrder', 'DeliveryOrder',
    'Product', 'Inventory', 'Supplier', 'Warehouse', 'PurchaseOrder',
    'Activity', 'ActivityReport'
]

