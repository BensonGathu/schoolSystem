from atexit import register
from django import template
from systemapp.models import Students
register = template.Library()




@register.simple_tag
def student_class_count(classID):
    qs = Students.objects.filter(student_class=classID)
    if qs.exists():
        return qs.count()
    return 0