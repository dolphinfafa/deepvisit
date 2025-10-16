# 外勤管理系统 (DeepVisit)

一个基于 Flask 的外勤管理系统后台 Demo，用于管理客户、拜访计划、订单和库存等业务。

## 功能模块

### 1. 客户管理
- **终端客户管理**：新增、查询、编辑、审批终端客户
- **直营商管理**：管理直营商客户信息
- **KOL管理**：管理KOL客户资源
- **客户联系人**：维护客户联系人信息

### 2. 外勤管理
- **拜访计划**：创建和管理拜访计划
- **拜访路线**：规划拜访路线
- **拜访记录**：记录拜访详情
- **外勤轨迹**：查看外勤人员轨迹

### 3. 订单管理
- **销售订单**：创建和管理销售订单
- **退货订单**：处理退货申请
- **发货订单**：管理发货流程

### 4. 库存管理
- **商品管理**：维护商品信息
- **库存查询**：查询各仓库库存

### 5. 系统管理
- **员工管理**：管理系统用户账号
- **角色管理**：配置角色和权限
- **审批管理**：配置审批流程

## 技术栈

- **后端框架**：Flask 3.0
- **数据库 ORM**：Flask-SQLAlchemy
- **用户认证**：Flask-Login
- **前端**：HTML5 + CSS3 + JavaScript
- **数据库**：SQLite (开发环境)

## 安装和运行

### 1. 环境要求
- Python 3.8+
- Conda (可选)

### 2. 安装依赖

使用 Conda 虚拟环境（推荐）：
```bash
# 创建虚拟环境
conda create -n deepvisit python=3.10
conda activate deepvisit

# 安装依赖
pip install -r requirements.txt
```

或使用 venv：
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 运行应用

```bash
# 在 deepvisit 虚拟环境下运行
conda activate deepvisit
python run.py
```

应用将在 http://localhost:5000 启动

### 4. 默认账号

- **用户名**：admin
- **密码**：admin123

## 项目结构

```
deepvisit/
├── app/
│   ├── __init__.py          # 应用初始化
│   ├── models/              # 数据模型
│   │   ├── user.py          # 用户模型
│   │   ├── role.py          # 角色模型
│   │   ├── customer.py      # 客户模型
│   │   ├── visit.py         # 拜访模型
│   │   ├── order.py         # 订单模型
│   │   ├── product.py       # 商品模型
│   │   └── inventory.py     # 库存模型
│   ├── routes/              # 路由视图
│   │   ├── auth.py          # 认证路由
│   │   ├── customer.py      # 客户管理路由
│   │   ├── visit.py         # 拜访管理路由
│   │   ├── order.py         # 订单管理路由
│   │   ├── inventory.py     # 库存管理路由
│   │   └── system.py        # 系统管理路由
│   └── templates/           # HTML 模板
├── config.py                # 配置文件
├── requirements.txt         # 依赖列表
├── run.py                   # 启动文件
└── README.md                # 说明文档
```

## 数据库

首次运行时会自动创建 SQLite 数据库和默认数据：
- 数据库文件：`deepvisit.db`
- 自动创建默认角色和管理员账号

## 开发说明

这是一个演示版本（Demo），主要功能包括：

1. ✅ 完整的用户认证系统
2. ✅ 客户管理（终端、直营商、KOL）
3. ✅ 基础的 CRUD 操作
4. ✅ 现代化的 UI 界面
5. 🚧 拜访管理（部分功能）
6. 🚧 订单管理（部分功能）
7. 🚧 库存管理（部分功能）

## 后续扩展

可以扩展的功能：
- [ ] 完善审批流程
- [ ] 添加数据导入导出
- [ ] 实现消息通知
- [ ] 移动端适配
- [ ] 数据统计和报表
- [ ] 地图定位功能
- [ ] 文件上传功能

## 许可证

MIT License

