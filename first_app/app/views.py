from flask_appbuilder import ModelView
from flask_appbuilder.fieldwidgets import Select2Widget
from flask_appbuilder.models.sqla.interface import SQLAInterface
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from . import appbuilder, db
from .models import Benefit, Department, Employee, EmployeeHistory, Function



from flask_appbuilder import AppBuilder, expose, BaseView
from app import appbuilder
from flask_appbuilder import has_access

from flask_appbuilder.security.registerviews import RegisterUserDBView
#from flask import Flask
from flask_babel import lazy_gettext
#from flask_mail import Mail, Message

class MyRegisterUserDBView(RegisterUserDBView):
    email_template = 'register_mail.html'
    email_subject = lazy_gettext('Your Account activation')
    activation_template = 'activation.html'
    form_title = lazy_gettext('Fill out the registration form')
    error_message = lazy_gettext('Not possible to register you at the moment, try again later')
    message = lazy_gettext('Registration sent to your email')
from flask_appbuilder.security.sqla.manager import SecurityManager
class MySecurityManager(SecurityManager):
    registeruserdbview = MyRegisterUserDBView




class MyView1(BaseView):
    default_view = 'hello'
 
    @expose('/hello/')
    @has_access
    def hello(self):
      return self.render_template('index.html')
 
appbuilder.add_view(MyView1, "Home Page", category='Home')






def department_query():
    return db.session.query(Department)


class EmployeeHistoryView(ModelView):
    datamodel = SQLAInterface(EmployeeHistory)
    # base_permissions = ['can_add', 'can_show']
    list_columns = ["department", "begin_date", "end_date"]


class EmployeeView(ModelView):
    datamodel = SQLAInterface(Employee)

    list_columns = ["full_name", "department.name", "employee_number"]
    edit_form_extra_fields = {
        "department": QuerySelectField(
            "Department",
            query_factory=department_query,
            widget=Select2Widget(extra_classes="readonly"),
        )
    }

    related_views = [EmployeeHistoryView]
    show_template = "appbuilder/general/model/show_cascade.html"


class FunctionView(ModelView):
    datamodel = SQLAInterface(Function)
    related_views = [EmployeeView]


class DepartmentView(ModelView):
    datamodel = SQLAInterface(Department)
    related_views = [EmployeeView]


class BenefitView(ModelView):
    datamodel = SQLAInterface(Benefit)
    add_columns = ["name"]
    edit_columns = ["name"]
    show_columns = ["name"]
    list_columns = ["name"]


db.create_all()

appbuilder.add_view_no_menu(EmployeeHistoryView, "EmployeeHistoryView")
appbuilder.add_view(
    EmployeeView, "Employees", icon="fa-folder-open-o", category="Company"
)
appbuilder.add_separator("Company")
appbuilder.add_view(
    DepartmentView, "Departments", icon="fa-folder-open-o", category="Company"
)
appbuilder.add_view(
    FunctionView, "Functions", icon="fa-folder-open-o", category="Company"
)
appbuilder.add_view(
    BenefitView, "Benefits", icon="fa-folder-open-o", category="Company"
)



from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .models import ContactGroup, Contact
from app import appbuilder, db
 
class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)
 
    label_columns = {'contact_group':'Contacts Group'}
    list_columns = ['name','personal_cellphone','birthday','contact_group']
 
    show_fieldsets = [
                        (
                            'Summary',
                            {'fields':['name','address','contact_group']}
                        ),
                        (
                            'Personal Info',
                            {'fields':['birthday','personal_phone','personal_cellphone'],'expanded':False}
                        ),
                     ]

class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]

db.create_all()
appbuilder.add_view(GroupModelView,
                    "List Groups",
                    icon = "fa-address-book-o",
                    category = "Contacts",
                    category_icon = "fa-envelope")
appbuilder.add_view(ContactModelView,
                    "List Contacts",
                    icon = "fa-address-card-o",
                    category = "Contacts")



from flask import render_template
from flask_appbuilder import ModelView, ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from wtforms.fields import TextField

from . import appbuilder, db
from .models import Region, District, Shop, DeliveryAddress, MallDollar, GiftCard, DiscountCode, PromoteCode
from .models import Order, OrderItem, Item, Brand, Supplier, Representative, Category, Origin, Purchase
from .models import CreditCardType, CreditCardPayment
from .models import SeasonItems, HotItems, NewItems, Festival, FestivalItems

class BS3TextFieldROWidget(BS3TextFieldWidget):
    def __call__(self, field, **kwargs):
        kwargs['readonly'] = 'true'
        return super(BS3TextFieldROWidget, self).__call__(field, **kwargs)
"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""


class RegionModelView(ModelView):
    datamodel = SQLAInterface(Region)

class DistrictModelView(ModelView):
    datamodel = SQLAInterface(District)
    list_columns = ["region", "name"]
    base_order = ("name", "asc")

class ShopModelView(ModelView):
    datamodel = SQLAInterface(Shop)

class DeliveryAddressModelView(ModelView):
    datamodel = SQLAInterface(DeliveryAddress)
    list_columns = ["user", "name", "room", "floor", "building", "street", "district"]
    add_columns = ["user", "name", "room", "floor", "building", "street", "district"]
    edit_columns = ["user", "name", "room", "floor", "building", "street", "district"]

class MallDollarModelView(ModelView):
    datamodel = SQLAInterface(MallDollar)

class GiftCardModelView(ModelView):
    datamodel = SQLAInterface(GiftCard)

class DiscountCodeModelView(ModelView):
    datamodel = SQLAInterface(DiscountCode)

class PromoteCodeModelView(ModelView):
    datamodel = SQLAInterface(PromoteCode)

class CreditCardTypeModelView(ModelView):
    datamodel = SQLAInterface(CreditCardType)

class CreditCardPaymentModelView(ModelView):
    datamodel = SQLAInterface(CreditCardPayment)

class BrandModelView(ModelView):
    datamodel = SQLAInterface(Brand)

class RepresentativeModelView(ModelView):
    datamodel = SQLAInterface(Representative)
    list_columns = ["supplier", "name", "tel"]

class PurchaseModelView(ModelView):
    datamodel = SQLAInterface(Purchase)
    list_columns = ["Date", "supplier", "item", "quantity", "price"]

class SupplierModelView(ModelView):
    datamodel = SQLAInterface(Supplier)
    related_views = [RepresentativeModelView]
    
class CategoryModelView(ModelView):
    datamodel = SQLAInterface(Category)
    
class OriginModelView(ModelView):
    datamodel = SQLAInterface(Origin)
    
class ItemModelView(ModelView):
    datamodel = SQLAInterface(Item)
    list_columns = ["category", "brand", "name", "origin", "price"]
    
class OrderItemModelView(ModelView):
    datamodel = SQLAInterface(OrderItem)
    list_columns = ["item", "quantity"]
    
class OrderModelView(ModelView):
    datamodel = SQLAInterface(Order)
    list_columns = ["number", "date", "staff", "customer"]
    base_order = ("date", "asc")
    edit_form_extra_fields = {
        "number": TextField("number", widget=BS3TextFieldROWidget()),
        "date": TextField("date", widget=BS3TextFieldROWidget()),
    }
    related_views = [OrderItemModelView, CreditCardPaymentModelView]
    
class SeasonItemsModelView(ModelView):
    datamodel = SQLAInterface(SeasonItems)
    list_columns = ["item"]

class HotItemsModelView(ModelView):
    datamodel = SQLAInterface(HotItems)
    list_columns = ["item"]
    
class NewItemsModelView(ModelView):
    datamodel = SQLAInterface(NewItems)
    list_columns = ["item"]
    
class FestivalItemsModelView(ModelView):
    datamodel = SQLAInterface(FestivalItems)
    list_columns = ["item", "item.price"]

class FestivalModelView(ModelView):
    datamodel = SQLAInterface(Festival)
    list_columns = ["name"]
    related_views = [FestivalItemsModelView]

appbuilder.add_view(RegionModelView, "Regions", icon="fa-map", category="Manage", category_icon="fa-envelope")
appbuilder.add_view(DistrictModelView, "Districts", icon="fa-location-arrow", category="Manage")
appbuilder.add_separator("Manage")
appbuilder.add_view(ShopModelView, "Shops", icon="fa-home", category="Manage")
appbuilder.add_view(GiftCardModelView, "Gift Cards", icon="fa-home", category="Manage")
appbuilder.add_view(DiscountCodeModelView, "Discount Codes", icon="fa-home", category="Manage")
appbuilder.add_view(PromoteCodeModelView, "Promote Codes", icon="fa-home", category="Manage")
appbuilder.add_separator("Manage")
appbuilder.add_view(BrandModelView, "Brands", icon="fa-globe", category="Manage")
appbuilder.add_view(SupplierModelView, "Suppliers", icon="fa-globe", category="Manage")
appbuilder.add_view(RepresentativeModelView, "Representatives", icon="fa-user", category="Manage")
appbuilder.add_view(PurchaseModelView, "Purchases", icon="fa-money", category="Manage")

appbuilder.add_view(CategoryModelView, "Categories", icon="fa-globe", category="Manage")
appbuilder.add_view(OriginModelView, "Origins", icon="fa-globe", category="Manage")
appbuilder.add_view(ItemModelView, "Items", icon="fa-money", category="Manage")
appbuilder.add_separator("Manage")
appbuilder.add_view(SeasonItemsModelView, "Season Items", icon="fa-home", category="Manage");
appbuilder.add_view(HotItemsModelView, "Hot Items", icon="fa-home", category="Manage");
appbuilder.add_view(NewItemsModelView, "New Items", icon="fa-home", category="Manage");
appbuilder.add_view_no_menu(FestivalItemsModelView)
appbuilder.add_view(FestivalModelView, "Festivals", icon="fa-home", category="Manage");
appbuilder.add_view(CreditCardTypeModelView, "Credit Card Types", icon="fa-home", category="Manage")

appbuilder.add_view(DeliveryAddressModelView, "Delivery Addresses", icon="fa-map-marker", category="Account", category_icon="fa-user")
appbuilder.add_view(MallDollarModelView, "Mall Dollars", icon="fa-money", category="Account", category_icon="fa-user")

appbuilder.add_view(OrderModelView, "Orders", icon="fa-money", category="Account", category_icon="fa-user")
appbuilder.add_view_no_menu(OrderItemModelView)
appbuilder.add_view_no_menu(CreditCardPaymentModelView)


"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )


db.create_all()