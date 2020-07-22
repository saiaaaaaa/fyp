import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship


from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from flask_appbuilder import Model
 

class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)
 
    def __repr__(self):
        return self.name

class Contact(Model):
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
    address =  Column(String(564))
    birthday = Column(Date)
    personal_phone = Column(String(20))
    personal_cellphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey('contact_group.id'))
    contact_group = relationship("ContactGroup")
 
    def __repr__(self):
        return self.name




class Department(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Function(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Benefit(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


assoc_benefits_employee = Table(
    "benefits_employee",
    Model.metadata,
    Column("id", Integer, primary_key=True),
    Column("benefit_id", Integer, ForeignKey("benefit.id")),
    Column("employee_id", Integer, ForeignKey("employee.id")),
)


def today():
    return datetime.datetime.today().strftime("%Y-%m-%d")


class EmployeeHistory(Model):
    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    department = relationship("Department")
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    employee = relationship("Employee")
    begin_date = Column(Date, default=today)
    end_date = Column(Date)


class Employee(Model):
    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    address = Column(Text(250), nullable=False)
    fiscal_number = Column(Integer, nullable=False)
    employee_number = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    department = relationship("Department")
    function_id = Column(Integer, ForeignKey("function.id"), nullable=False)
    function = relationship("Function")
    benefits = relationship(
        "Benefit", secondary=assoc_benefits_employee, backref="employee"
    )

    begin_date = Column(Date, default=datetime.date.today(), nullable=True)
    end_date = Column(Date, default=datetime.date.today(), nullable=True)

    def __repr__(self):
        return self.full_name


from flask import Markup, url_for
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import ImageColumn
from flask_appbuilder.filemanager import ImageManager
from sqlalchemy import Column, Boolean, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime, time

"""
You can use the extra Flask-AppBuilder fields and Mixin's
AuditMixin will add automatic timestamp of created and modified by who
"""

class Region(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class District(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)
    region_id = Column(Integer, ForeignKey("region.id"))
    region = relationship("Region")

    def __repr__(self):
        return self.region.name + " > " + self.name

class DeliveryAddress(Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("ab_user.id"))
    user = relationship("User")
    name = Column(String(50))
    room = Column(String(50))
    floor = Column(String(50))
    building = Column(String(50))
    street = Column(String(50))
    district_id = Column(Integer, ForeignKey("district.id"))
    district = relationship("District")

    def __repr__(self):
        return self.name

class Shop(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)
    address = Column(String(200))
    pickup = Column(Boolean)
    district_id = Column(Integer, ForeignKey("district.id"))
    district = relationship("District")

    def __repr__(self):
        return self.name

class MallDollar(Model):
    user_id = Column(Integer, ForeignKey("ab_user.id"), primary_key=True)
    user = relationship("User")
    amount = Column(Float(5,2))

    def __repr__(self):
        return "Mall $" + self.amount

class GiftCard(Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique = True, nullable=False)
    description = Column(String(500))
    amount = Column(Float(5,2))

    def __repr__(self):
        return "Gift $" + self.amount

class GiftCardSold(Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("ab_user.id"))
    user = relationship("User")
    gift_card_id = Column(Integer, ForeignKey("gift_card.id"))
    gift_card = relationship("GiftCard")
    purchase_order_id = Column(Integer, ForeignKey("order.id"))
    purchase_order = relationship("Order", foreign_keys=[purchase_order_id]);
    redeem_order_id = Column(Integer, ForeignKey("order.id"))
    redeem_order = relationship("Order", foreign_keys=[redeem_order_id]);

    def __repr__(self):
        return "Gift $" + self.gift_card.amount

class DiscountCode(Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique = True, nullable=False)
    description = Column(String(500))
    rate = Column(Float(4,2))
    min_amount = Column(Float(5,2))

    def __repr__(self):
        return self.code

class DiscountCodeUsed(Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("ab_user.id"))
    user = relationship("User")
    discount_code_id = Column(Integer, ForeignKey("discount_code.id"))
    discount_code = relationship("DiscountCode")
    redeem_order_id = Column(Integer, ForeignKey("order.id"))
    redeem_order = relationship("Order", foreign_keys=[redeem_order_id]);
    
    def __repr__(self):
        return self.code

class PromoteCode(Model):
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique = True, nullable=False)
    description = Column(String(500))
    amount = Column(Float(5,2))

    def __repr__(self):
        return self.code

class CreditCardType(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name
        
class CreditCardPayment(Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.datetime.now().replace(microsecond=0))
    order_id = Column(Integer, ForeignKey("order.id"))
    order = relationship("Order")
    credit_card_type_id = Column(Integer, ForeignKey("credit_card_type.id"))
    credit_card_type = relationship("CreditCardType")
    card_number = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    
    def __repr__(self):
        return self.card_number
        
class PromoteCodeUsed(Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("ab_user.id"))
    user = relationship("User")
    promote_code_id = Column(Integer, ForeignKey("promote_code.id"))
    promote_code = relationship("PromoteCode")
    redeem_order_id = Column(Integer, ForeignKey("order.id"))
    redeem_order = relationship("Order", foreign_keys=[redeem_order_id]);
    
    def __repr__(self):
        return self.promote_code.code

class Brand(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)
    homepage = Column(String(500))
    
    def __repr__(self):
        return self.name
        
class Supplier(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)
    
    def __repr__(self):
        return self.name        
        
class Representative(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)
    tel = Column(String(50))
    supplier_id = Column(Integer, ForeignKey("supplier.id"), nullable=False)
    supplier = relationship("Supplier", foreign_keys=[supplier_id])
    
    def __repr__(self):
        return self.name        
        
class Purchase(Model):
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False, default=datetime.datetime.now().replace(microsecond=0))
    supplier_id = Column(Integer, ForeignKey("supplier.id"), nullable=False)
    supplier = relationship("Supplier", foreign_keys=[supplier_id])
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    item = relationship("Item", foreign_keys=[item_id])
    price = Column(Float, nullable=False)
    quantity= Column(Integer, nullable=False)
    
    def __repr__(self):
        return self.name        
        
class Category(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)
    
    def __repr__(self):
        return self.name
        
class Origin(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)
    
    def __repr__(self):
        return self.name
        
class Item(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique = True, nullable=False)
    price = Column(Float, nullable=False)
    photo = Column(ImageColumn(size=(300, 300, True), thumbnail_size=(30, 30, True)))
    
    brand_id = Column(Integer, ForeignKey("brand.id"), nullable=False)
    brand = relationship("Brand", foreign_keys=[brand_id])
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    category = relationship("Category", foreign_keys=[category_id])
    origin_id = Column(Integer, ForeignKey("origin.id"), nullable=False)
    origin = relationship("Origin", foreign_keys=[origin_id])
    
    def photo_imgage(self):
        im = ImageManager()
        if self.photo:
            return Markup('<a href="' + url_for('PersonModelView.show',pk=str(self.id)) + '" class="thumbnail"><img src="' + im.get_url(self.photo) + '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="' + url_for('PersonModelView.show',pk=str(self.id)) + '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')

    def photo_thumbnail(self):
        im = ImageManager()
        if self.photo:
            return Markup('<a href="' + url_for('PersonModelView.show',pk=str(self.id)) + '" class="thumbnail"><img src="' + im.get_url_thumbnail(self.photo) + '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="' + url_for('PersonModelView.show',pk=str(self.id)) + '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')
    
    def __repr__(self):
        return self.name + " ($" + str(self.price) + ")"

class Order(Model):
    id = Column(Integer, primary_key=True)
    number = Column(String(20), unique=True, nullable=False, default=int(round(time.time() * 1000)))
    date = Column(DateTime, nullable=False, default=datetime.datetime.now().replace(microsecond=0))
    
    staff_id = Column(Integer, ForeignKey("ab_user.id"), nullable=False)
    staff = relationship("User", foreign_keys=[staff_id])
    customer_id = Column(Integer, ForeignKey("ab_user.id"), nullable=False)
    customer = relationship("User", foreign_keys=[customer_id])
    
    delivery_address_id = Column(Integer, ForeignKey("delivery_address.id"), nullable=False)
    delivery_address = relationship("DeliveryAddress", foreign_keys=[delivery_address_id])
    
    def __repr__(self):
        return self.number

class OrderItem(Model):
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)

    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    order = relationship("Order", foreign_keys=[order_id])
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    item = relationship("Item", foreign_keys=[item_id])

class Payment(Model):
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    order = relationship("Order", foreign_keys=[order_id])

    def __repr__(self):
        return self.promote_code.code

class SeasonItems(Model):
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    item = relationship("Item", foreign_keys=[item_id])
    
    def __repr__(self):
        return self.item.name

class HotItems(Model):
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    item = relationship("Item", foreign_keys=[item_id])
    
    def __repr__(self):
        return self.item.name

class NewItems(Model):
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    item = relationship("Item", foreign_keys=[item_id])
    
    def __repr__(self):
        return self.item.name

class Festival(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

class FestivalItems(Model):
    id = Column(Integer, primary_key=True)
    festival_id = Column(Integer, ForeignKey("festival.id"), nullable=False)
    festival = relationship("Festival", foreign_keys=[festival_id])
    item_id = Column(Integer, ForeignKey("item.id"), nullable=False)
    item = relationship("Item", foreign_keys=[item_id])
    
    def __repr__(self):
        return self.item.name
