from atexit import register
from django import template
from systemapp.models import Students,Classes,Subjects
register = template.Library()



#returns the number of students in a certain class
@register.simple_tag
def student_class_count(classID):
    qs = Students.objects.filter(student_class=classID)
    return qs.count()
    



#returns the number of subjects that a teacher is teaching
@register.simple_tag
def teacher_subject_count(teacherID):
    qs = Subjects.objects.filter(staff_id=teacherID)
    print(qs)
    if qs.exists():
        return qs.count()
    return 0


#returns the class that a certain staff is the class teacher of 
@register.simple_tag
def teacher_class(teacherID):
    qs = Classes.objects.filter(class_teacher=teacherID)
    for clas in qs:
        return clas.name
  

  #returns the number of students taking a certain subect
@register.simple_tag
def student_count(subjectID):
    student_list = []
    try:
        all_students = Students.objects.all()
        for student in all_students:
            for subjects in student.subject_id.all():
                
                if subjects.id == subjectID:
                    student_list.append(student)
                   

        print(student_list)
        return len(student_list)

        

    except:
        return 0
      