from atexit import register
from django import template
from systemapp.models import Students,Classes,Subjects,StudentResult
register = template.Library()


#returns number of subjects/lessons that a staff is teaching
@register.simple_tag
def subjects_count(staffID):
    qs = Subjects.objects.filter(staff_id=staffID)
    return qs.count()



#returns the classes that a staff is teaching 
@register.simple_tag
def classes_count(staffID):
    qs = Classes.objects.filter(sessionperiod=staffID)
    return qs.count()


#returns the classes that a staff is classteacher of 
@register.simple_tag
def classes_count(staffID):
    classes_list = []
    try:
        classteacher_to = Classes.objects.filter(class_teacher=staffID)
        for classess in classteacher_to:
            single_class = classess.name, classess.sessionperiod.school_term
            classes_list.append(single_class)
            return classes_list

    except:
        return None
    

#returns the number of students that a staff is teaching
@register.simple_tag
def student_count(staffID):
    student_list = []
    try:
        all_students = Students.objects.all()
        for student in all_students:
            for subjects in student.subject_id.all():
                if subjects.staff_id == staffID:
                    student_list.append(student)
                   
            
        return len(set(student_list))

        

    except:
        return 0
      


@register.simple_tag
def get_student_marks(studentID,subjectID):
    try:
        results = StudentResult.objects.get(student_id=studentID,subject_id=subjectID)
        return results
    except:
        return None