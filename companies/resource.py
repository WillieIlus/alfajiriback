from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .models import Company
from locations.models import Location
from categories.models import Category
from accounts.models import User


class CompanyResource(resources.ModelResource):
    name = fields.Field(attribute='name', column_name='Name')
    location = fields.Field(attribute='location', column_name='Location', widget=ForeignKeyWidget(Location, 'name'))
    address = fields.Field(attribute='address', column_name='Address')
    category = fields.Field(attribute='category', column_name='Category', widget=ForeignKeyWidget(Category, 'name'))
    email = fields.Field(attribute='email', column_name='Email')
    website = fields.Field(attribute='website', column_name='Website')
    phone = fields.Field(attribute='phone', column_name='Phone')
    logo = fields.Field(attribute='image', column_name='Logo')
    user = fields.Field(attribute='user', column_name='User', widget=ForeignKeyWidget(User, 'email'))
    description = fields.Field(attribute='description', column_name='Description')


    class Meta:
        model = Company
        fields = ('id', 'name', 'location', 'address', 'category', 'company', 'email', 'website', 'phone', 'logo', 'user', 'description')
        export_order = fields
