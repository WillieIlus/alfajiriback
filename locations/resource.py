from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .models import Location


class LocationResource(resources.ModelResource):
    name = fields.Field(attribute='name', column_name='Name')
    description = fields.Field(attribute='description', column_name='Description')


    class Meta:
        model = Location
        fields = ('id', 'name', 'description')
        export_order = fields
