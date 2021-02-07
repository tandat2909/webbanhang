from API import db
from sqlalchemy import Column, DATETIME, String, INTEGER, ForeignKey, Float, BOOLEAN, Enum as EnumSQL
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import UUIDType, EmailType
import uuid
import datetime
from enum import Enum


# ==============Enum======================================#
class EStatusFunction(Enum):
    active = "Active"
    in_active = "InActive"
    warning = "Warning"


class EStatusOrder(Enum):
    paid = 'Đã thanh toán hóa đơn'
    unpaid = 'Chưa thanh toán hóa đơn'
    wait_pay = 'Chờ thanh toán hóa đơn'


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(UUIDType(binary=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), default="")

    def __str__(self):
        return str(self.id) + "_" + self.name


class Identification(BaseModel):
    """
        lớp chứa thông tin cá nhân
        class information person
    """
    __tablename__ = "Identification"
    avatar = Column(String(300), default="")
    first_name = Column(String(50), default="")
    last_name = Column(String(50), default="")
    birthday = Column(DATETIME)
    CMND_CCCD = Column(String(50), default="")
    birthplace = Column(String(100), default="")
    email = Column(EmailType, default="")
    phonenumber = Column(String(30), default="")
    address = Column(String(200), default="")
    # relationship
    customer = relationship('Customer', backref='identification', uselist=False, lazy=True)
    employee = relationship('Employee', backref='identification', uselist=False, lazy=True)


# =========== System =======================================#

class Configuration(db.Model):
    __tablename__ = "Configuration"
    key = Column(String(50), nullable=False, primary_key=True)
    value = Column(String(100), nullable=False)


class Role(BaseModel):
    __tablename__ = "Role"
    description = Column(String(500), default="")

    # relationship
    users = relationship('Account', backref='role', lazy=True)
    # accounts = relationship('Account', secondary='AccountRole', backref=backref("role", lazy=True))
    permissions = relationship('Permission', backref='role', lazy=True)
    # end relationship


class Function(BaseModel):
    __tablename__ = "Function"
    parent_id = Column(UUIDType(binary=True), default=None)
    url = Column(String(500), default="")
    status = Column(EnumSQL(EStatusFunction), default=EStatusFunction.in_active)

    # relationship
    permissions = relationship('Permission', backref='function', lazy=True)


class Action(BaseModel):
    __tablename__ = 'Action'
    # relationship
    permissions = relationship('Permission', backref='action', lazy=True)


class Permission(BaseModel):
    __tablename__ = 'Permission'
    description = Column(String(300), default="")
    role_id = Column(UUIDType(binary=True), ForeignKey('Role.id'))
    action_id = Column(UUIDType(binary=True), ForeignKey('Action.id'))
    function_id = Column(UUIDType(binary=True), ForeignKey('Function.id'))


class AccountRole(db.Model):
    __tablename__ = "AccountRole"
    role_id = Column(UUIDType(binary=True), ForeignKey('Role.id'), primary_key=True)
    account_id = Column(UUIDType(binary=True), ForeignKey('Account.id'), primary_key=True)


class Account(BaseModel):
    __tablename__ = "Account"
    name = None
    username = Column(String(50), nullable=False)
    password = Column(String(600), nullable=False)
    join_date = Column(DATETIME, nullable=False, default=datetime.datetime.now())

    # relationship
    employee = relationship('Employee', backref='account', uselist=False)
    customer = relationship('Customer', backref='account', uselist=False)
    roles = relationship('Role', secondary='AccountRole', lazy='subquery', backref=backref('account', lazy=True))

    def __str__(self):
        return self.username


class Employee(BaseModel):
    """
        class create table,column databaser user
        :extends BaseModel, Contact, information
    """
    __tablename__ = "Employee"
    name = None
    account_id = Column(UUIDType(binary=True), ForeignKey("Account.id"), primary_key=True)
    identification_id = Column(UUIDType(binary=True), ForeignKey('Identification.id'), primary_key=True)
    # relationship
    orders = relationship('Order', backref='employee', lazy=True)
    roles = relationship('Role', secondary='AccountRole', backref=backref('employee', lazy=True))

    # end relationship


class Customer(BaseModel):
    __tablename__ = "Customer"
    name = None
    account_id = Column(UUIDType(binary=True), ForeignKey("Account.id"), primary_key=True)
    identification_id = Column(UUIDType(binary=True), ForeignKey('Identification.id'), primary_key=True)
    # relationship

    orders = relationship('Order', backref='customer', lazy=True)
    roles = relationship('Role', secondary='AccountRole', backref=backref('customer', lazy=True))


class Product(BaseModel):
    __tablename__ = "Product"
    code = Column(String(100), default="")
    image = Column(String(500), default="")
    description = Column(String(500), default="")
    price = Column(Float, nullable=False, default=0)
    stock = Column(INTEGER, nullable=False, default=0)
    categorize_id = Column(UUIDType(binary=True), ForeignKey("Categories.id"), nullable=False)


class Categories(BaseModel):
    __tablename__ = "Categories"
    isShowHome = Column(BOOLEAN, default=False)
    parent_id = Column(UUIDType(binary=True), default=None)

    # relationship
    products = relationship('Product', backref='categories', lazy=True)


class UnitPrice(BaseModel):
    __tablename__ = 'UnitPrice'
    value = Column(Float, default=0)


class Order(db.Model):
    __tablename__ = "Order"
    id = Column(String(100), primary_key=True, nullable=False)
    order_date = Column(DATETIME, default=datetime.datetime.now())
    paid_date = Column(DATETIME)
    amount_money = Column(Float, default=0)

    # relationship

    order_detail = relationship('OrderDetail', backref='order', lazy=True)

    # ForeignKey
    employee_id = Column(UUIDType(binary=True), ForeignKey('Employee.id'), nullable=False)
    customer_id = Column(UUIDType(binary=True), ForeignKey('Customer.id'), nullable=False)
    status = Column(EnumSQL(EStatusOrder), default=EStatusOrder.wait_pay)


class OrderDetail(db.Model):
    __tablename__ = "OrderDetail"
    id = Column(String(200), primary_key=True)
    order_id = Column(String(200), ForeignKey('Order.id'), nullable=False)
    product_id = Column(UUIDType(binary=True), ForeignKey('Product.id'), nullable=True)
    quantity = Column(INTEGER, default=1)
    price = Column(Float, default=0)
    unit_price = Column(UUIDType(binary=True), ForeignKey('UnitPrice.id'), nullable=False)




if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    print("success create tabel")
