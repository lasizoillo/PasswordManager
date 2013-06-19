from django.contrib.auth.models import User
from django.core.signing import BadSignature
from django.db import models
from passManager.functions import passEncr

class BaseSignedField(models.Field):
    """
    This is not a reusable or secure field. For a better implementation go to
    https://github.com/django-extensions/django-extensions/blob/master/django_extensions/db/fields/encrypted.py
    """
    def to_python(self, value):
        try:
            return passEncr('decrypt', value)
        except BadSignature:
            return value

    def get_db_prep_value(self, value, connection, prepared=False):
        print "get_db_prep_value"
        return value if value is None else passEncr('encrypt', value)

class SignedCharField(BaseSignedField):
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        defaults = {'max_length': self.max_length}
        defaults.update(kwargs)
        return super(SignedCharField, self).formfield(**defaults)

class passDb(models.Model):
    class Meta:
        verbose_name = 'Password'
        
    name = models.CharField(max_length=100)
    login = models.CharField(max_length=50)
    password = SignedCharField(max_length=100)
    server = models.CharField(max_length=60)
    date = models.DateField(auto_now=True)
    uploader = models.ForeignKey(User)
    notes = models.TextField()
 
    def __unicode__(self):
        return self.name
    
    def getClickMe(self):
        #password = passEncr('decrypt', self.password)
        idrow = self.id
        return '<font color="red"><span id=\"%s\" onClick=\"cambiar(\'%s\',\'%s\');\">ClickME</span></font>' % (idrow, idrow, self.password)
    getClickMe.allow_tags = True
    getClickMe.short_description = "Password"
    
    def _get_password(self):
        if len(self.password) != 0:
            password = passEncr('decrypt', self.password)
        else:
            password = ""
        return password
    


    
