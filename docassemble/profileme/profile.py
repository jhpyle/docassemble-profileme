from docassemble.base.util import as_datetime, DAObject, DAList, Individual, DAStore
import json

__all__ = ['Profile']

class Profile(DAObject):
  def init(self, *pargs, **kwargs):
    super().init(*pargs, **kwargs)
    self.initializeAttribute('store', DAStore)
  def export_to_server(self):
    self.store.set('profileme', self.as_data())
  def exists_on_server(self):
    return self.store.defined('profileme')
  def import_from_server(self):
    self.data = self.store.get('profileme') or dict()
  def import_from_json(self, text):
    self.data = json.loads(text)
  def import_from_file(self, file_obj):
    with open(file_obj.path(), 'r', encoding='utf-8') as fp:
      self.data = json.load(fp)
  def as_json(self):
    return json.dumps(self.as_data())
  def as_data(self):
    return self.data
  def update(self, obj, hh):
    self.data = self.individual_as_data(obj)
    self.data['household'] = list()
    for item in hh:
      member = self.individual_as_data(item)
      try:
        member['roleName'] = item.role
      except:
        pass
      self.data['household'].append(member)
  def individual_as_data(self, obj):
    data = {"@type": "Person"}
    try:
      data['name'] = obj.name.full()
    except:
      pass
    try:
      data['givenName'] = obj.name.first
    except:
      pass
    try:
      data['familyName'] = obj.name.last
    except:
      pass
    try:
      data['additionalName'] = obj.name.middle
    except:
      pass
    try:
      data['birthDate'] = obj.birthdate.format_date("yyyy-MM-dd")
    except:
      pass
    try:
      data['isVeteran'] = True if obj.is_veteran else False
    except:
      pass
    return data
  def populate_individual(self, obj, data):
    if 'givenName' in data:
      obj.name.first = data['givenName']
    elif 'name' in data:
      obj.name.uses_parts = False
      obj.name.text = data['name']
    if 'familyName' in data:
      obj.name.last = data['familyName']
    if 'additionalName' in data:
      obj.name.middle = data['additionalName']
    if 'birthDate' in data:
      obj.birthdate = as_datetime(data['birthDate'])
    if 'isVeteran' in data:
      obj.is_veteran = True if data['isVeteran'] else False
  def populate(self, obj, hh):
    self.populate_individual(obj, self.data)
    if 'household' in self.data:
      hh.clear()
      for item in self.data['household']:
        member = hh.appendObject()
        self.populate_individual(member, item)
        if 'roleName' in item:
          member.role = item['roleName']
      hh.gathered = True