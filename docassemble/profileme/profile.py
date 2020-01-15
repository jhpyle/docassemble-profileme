from docassemble.base.util import as_datetime, DAObject, DAList, Individual, DAStore
import json
<<<<<<< HEAD
from stegano import lsb
=======
>>>>>>> quinten/master

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
<<<<<<< HEAD
  def write_image(self, base_image, final_image):
    secret = lsb.hide(base_image.path(), self.as_json())
    secret.save(final_image.path())
    final_image.commit()
  def import_from_image(self, file_obj):
    self.import_from_json(lsb.reveal(file_obj.path()))
=======
>>>>>>> quinten/master
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
<<<<<<< HEAD
        member['roleName'] = item.relationship
=======
        member['roleName'] = item.role
>>>>>>> quinten/master
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
<<<<<<< HEAD
    try:
      data['veteranStatus'] = obj.veteran_status
    except:
      pass
    try:
      data['language'] = obj.language
    except:
      pass
    if hasattr(obj, 'address') and hasattr(obj.address, 'address'):
      try:
        data['address'] = {"@type": "PostalAddress"}
        data['address']['addressLocality'] = obj.address.city
        data['address']['addressRegion'] = obj.address.state
        if hasattr(obj.address, 'zip'):
          data['address']['postalCode'] = obj.address.zip
        data['address']['streetAddress'] = obj.address.address
        if hasattr(obj.address, 'unit'):
          data['address']['addressUnit'] = obj.address.unit
      except:
        pass
=======
>>>>>>> quinten/master
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
<<<<<<< HEAD
    if 'veteranStatus' in data:
      obj.veteran_status = data['veteranStatus']
    if 'language' in data:
      obj.language = data['language']
    if 'address' in data:
      if 'addressLocality' in data['address']:
        obj.address.city = data['address']['addressLocality']
      if 'addressRegion' in data['address']:
        obj.address.state = data['address']['addressRegion']
      if 'postalCode' in data['address']:
        obj.address.zip = data['address']['postalCode']
      if 'streetAddress' in data['address']:
        obj.address.address = data['address']['streetAddress']
      if 'addressUnit' in data['address']:
        obj.address.unit = data['address']['addressUnit']
=======
>>>>>>> quinten/master
  def populate(self, obj, hh):
    self.populate_individual(obj, self.data)
    if 'household' in self.data:
      hh.clear()
      for item in self.data['household']:
        member = hh.appendObject()
        self.populate_individual(member, item)
        if 'roleName' in item:
<<<<<<< HEAD
          member.relationship = item['roleName']
=======
          member.role = item['roleName']
>>>>>>> quinten/master
      hh.gathered = True