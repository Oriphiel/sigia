select array_to_json(array_agg(row_to_json(t)))
    from (
	SELECT
	  sigia_studentevent.id, 
	  to_char(sigia_studentevent.created, 'DD/MM/YY HH12:MI') as created,
	  to_char(sigia_studentevent.modified, 'DD/MM/YY HH12:MI') as modified,
	  created_user.username AS created_by, 
	  modified_user.username AS modified_by, 
	  student_user.last_name || ', ' || student_user.first_name AS student,
	  sigia_eventtype.name AS type, 
	  to_char(sigia_studentevent.start_date, 'DD/MM/YY') as start_date,
	  to_char(sigia_studentevent.end_date, 'DD/MM/YY') as end_date,
	  sigia_studentevent.ini_obs, 
	  sigia_studentevent.state, 
	  sigia_studentevent.end_obs,
	  teacher_user.last_name || ', ' || teacher_user.first_name AS teacher, 
	  manager_user.last_name || ', ' || manager_user.first_name AS manager
	FROM 
	  public.auth_user student_user, 
	  public.auth_user teacher_user, 
	  public.auth_user manager_user, 
	  public.sigia_student, 
	  public.auth_user created_user, 
	  public.auth_user modified_user, 
	  public.sigia_teacher, 
	  public.sigia_studentevent, 
	  public.sigia_eventtype
	WHERE 
	  student_user.id = sigia_student.user_id AND
	  created_user.id = sigia_studentevent.created_by_id AND
	  modified_user.id = sigia_studentevent.modified_by_id AND
	  manager_user.id = sigia_studentevent.manager_id AND
	  sigia_teacher.user_id = teacher_user.id AND
	  sigia_teacher.id = sigia_studentevent.tutor_id AND
	  sigia_studentevent.student_id = sigia_student.id AND
	  sigia_eventtype.id = sigia_studentevent.type_id
) t