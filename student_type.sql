UPDATE public.sigia_student SET 
  type = 'PRE'
FROM 
  public.sigia_enrollment, 
  public.auth_user, 
  public.sigia_course
WHERE 
  sigia_student.id = sigia_enrollment.student_id AND
  sigia_enrollment.course_id = sigia_course.id AND
  auth_user.id = sigia_student.user_id AND
  sigia_course.level = 0
