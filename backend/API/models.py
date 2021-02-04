from API import db
from sqlalchemy import Column, DATETIME, String, INTEGER, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import UUIDType, EmailType
import uuid
import datetime


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(UUIDType(binary=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), default="")

    def __str__(self):
        return str(self.id) + "_" + self.name


class Identification:
    """
        lớp chứa thông tin cá nhân
        class information person
    """
    avatar = Column(String(300), default="")
    first_name = Column(String(50), default="")
    last_name = Column(String(50), default="")
    birthday = Column(DATETIME)
    CMND_CCCD = Column(String(50), default="")
    birthplace = Column(String(100), default="")
    email = Column(EmailType, default="")
    phonenumber = Column(String(30), default="")
    address = Column(String(200), default="")


class Account(BaseModel):
    __abstract__ = True
    name = None
    username = Column(String(50), nullable=False)
    password = Column(String(600), nullable=False)
    joindate = Column(DATETIME, nullable=False, default=datetime.datetime.now())
    # ForeignKey
    role_id = Column(UUIDType(binary=True), ForeignKey("Role.id"), nullable=False)
    # endForeignKey
    def __str__(self):
        return self.username


class Employee(Account, Identification):
    """
        class create table,column databaser user
        :extends BaseModel, Contact, information
    """
    __tablename__ = "Employee"
    # relationship
    # end relationship

class Customer(Account,Identification):
    __tablename__ ="Customer"


class Role(BaseModel):
    __tablename__ = "Role"
    description = Column(String(500), default="")

    # relationship
    users = relationship('Account', backref='role', lazy=True)
    # end relationship


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    print("success create tabel")
