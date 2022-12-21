from atexit import register
from django import template
from systemapp.models import Students,Classes,Subjects,StudentResult
register = template.Library()


@register.simple_tag
def get_results_added(studentID):
    try:
        student_result = StudentResult.objects.filter(student_id=studentID).count()
        return student_result
    except:
        return 0

@register.simple_tag
def get_position(subjectID):
    all_results = []
    results = StudentResult.objects.filter(subject_id=subjectID)
    for result in results:
        single_result =  (result.student_id, result.mean_marks)
        all_results.append(single_result)

    print(all_results)
   