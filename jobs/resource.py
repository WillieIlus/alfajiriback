from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .models import Job
from companies.models import Company
from locations.models import Location
from categories.models import Category
from accounts.models import User


class JobResource(resources.ModelResource):
    title = fields.Field(attribute='title', column_name='Title')
    location = fields.Field(attribute='location', column_name='Location', widget=ForeignKeyWidget(Location, 'name'))
    address = fields.Field(attribute='address', column_name='Address')
    category = fields.Field(attribute='category', column_name='Category', widget=ForeignKeyWidget(Category, 'name'))
    company = fields.Field(attribute='company', column_name='Company', widget=ForeignKeyWidget(Company, 'name'))
    email = fields.Field(attribute='email', column_name='Email')
    website = fields.Field(attribute='website', column_name='Website')
    phone = fields.Field(attribute='phone', column_name='Phone')
    image = fields.Field(attribute='image', column_name='Image')
    user = fields.Field(attribute='user', column_name='User', widget=ForeignKeyWidget(User, 'email'))
    description = fields.Field(attribute='description', column_name='Description')
    requirements = fields.Field(attribute='requirements', column_name='Requirements')
    responsibilities = fields.Field(attribute='responsibilities', column_name='Responsibilities')
    job_type = fields.Field(attribute='job_type', column_name='Job Type')
    salary = fields.Field(attribute='salary', column_name='Salary')
    work_experience = fields.Field(attribute='work_experience', column_name='Work Experience')
    education_level = fields.Field(attribute='education_level', column_name='Education Level')
    applicants = fields.Field(attribute='applicants', column_name='Applicants', widget=ManyToManyWidget(User, 'email'))

    class Meta:
        model = Job
        fields = (
            'id', 'title', 'location', 'address', 'category', 'company', 'email', 'website', 'phone',
            'image', 'user', 'description', 'requirements', 'responsibilities', 'job_type',
            'salary', 'work_experience',  'education_level', 'applicants')
        export_order = fields
