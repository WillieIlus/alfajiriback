from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .models import Category
from accounts.models import User


class CategoryResource(resources.ModelResource):
    name = fields.Field(attribute='name', column_name='Name')
    description = fields.Field(attribute='description', column_name='Description')


    class Meta:
        model = Category
        fields = ('id', 'name', 'description')
        export_order = fields