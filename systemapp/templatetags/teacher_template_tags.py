from atexit import register
from django import template
from django.shortcuts import get_object_or_404
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

@register.simple_tag
def get_students_per_subject(subjectID):
    # current_subject = get_object_or_404(Subjects,id=subjectID)
    students = []
    all_students =  Students.objects.all()
    for student in all_students:
        for subject in student.subject_id.all():
            if subject.id == int(subjectID):
                students.append(student)
    return len(students)


@register.simple_tag
def get_student_subject(studentID,staffID):
    student_obj = get_object_or_404(Students,id=studentID)
    subjects = []
    for subject in student_obj.subject_id.all():
        if subject.staff_id.id == int(staffID):
            subjects.append(subject)
            return subject
        



@register.simple_tag
def student_subject_positions(id):
    all_info = subjectInfo.objects.filter(subject=id).order_by("-mean_marks")
    
    for i,info in enumerate(all_info):
        info.position = i+1 
        info.save()
        
    return redirect("students",id)
    

