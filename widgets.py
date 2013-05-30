from django.contrib.admin.widgets import AdminTextInputWidget
from django.utils.safestring import mark_safe

class AccessTokenWidget(AdminTextInputWidget):

    def __init__(self, attrs=None):
        final_attrs = {'class': 'vTextField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminTextInputWidget, self).__init__(attrs=final_attrs)
        
    def render(self, name, value, attrs=None):
        output = []
        output.append(super(AdminTextInputWidget, self).render(name, value, attrs))
        if not value:
            output.append('<button><a href="/linkedin" onclick="return showAddAnotherPopup(this);">Ottieni access_token Linkedin</a></button>')
        return mark_safe(u''.join(output))
