from django import template
register = template.Library()

# @register.filter(name="kesish")

def adminManager(value):
    # print(value.groups.exists())
    allowed_roles = ['admin', 'manager']
    group = None
    if value.groups.exists():
        group = value.groups.all()[0].name

    if group in allowed_roles:
        return True
    else:
        return False

register.filter('adminManager', adminManager)
