from testapiclient.models import base_modal as base


class ProjectCreateRequest(base.BaseModel):
    def __init__(self, name='', description=''):
        self.description = description
        self.name = name


class Project(ProjectCreateRequest):
    def __init__(
        self, _id='', creation_date='', creator='',
        name='', description=''):
        self._id = _id
        self.creation_date = creation_date
        self.creator = creator
        super(Project, self).__init__(name, description)
