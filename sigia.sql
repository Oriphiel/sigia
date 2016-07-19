BEGIN;
CREATE TABLE "sigia_period" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "name" varchar(9) NOT NULL UNIQUE,
    "predecessor_id" integer REFERENCES "sigia_period" ("id") DEFERRABLE INITIALLY DEFERRED,
    "finalized" boolean NOT NULL,
    "active" boolean NOT NULL,
    "start_notes" text,
    "end_notes" text
)
;

CREATE TABLE "sigia_country" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "name" varchar(50) NOT NULL UNIQUE,
    "gentilicio" varchar(50) NOT NULL
)
;

CREATE TABLE "sigia_province" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "country_id" integer NOT NULL REFERENCES "sigia_country" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(50) NOT NULL
)
;
CREATE TABLE "sigia_canton" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "province_id" integer NOT NULL REFERENCES "sigia_province" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(50) NOT NULL
)
;
CREATE TABLE "sigia_parish" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "canton_id" integer NOT NULL REFERENCES "sigia_canton" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(50) NOT NULL
)
;
CREATE TABLE "sigia_ethnicgroup" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "name" varchar(50) NOT NULL,
    "description" varchar(100)
)
;
CREATE TABLE "sigia_institution" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "name" varchar(100) NOT NULL
)
;
CREATE TABLE "sigia_userprofile" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "photo" varchar(100),
    "id_doc_type" varchar(1),
    "id_doc_num" varchar(20),
    "gender" varchar(1),
    "birthday" date,
    "nationality_id" integer REFERENCES "sigia_country" ("id") DEFERRABLE INITIALLY DEFERRED,
    "birthplace_country_id" integer REFERENCES "sigia_country" ("id") DEFERRABLE INITIALLY DEFERRED,
    "birthplace_province_id" integer REFERENCES "sigia_province" ("id") DEFERRABLE INITIALLY DEFERRED,
    "birthplace_canton_id" integer REFERENCES "sigia_canton" ("id") DEFERRABLE INITIALLY DEFERRED,
    "birthplace_parish_id" integer REFERENCES "sigia_parish" ("id") DEFERRABLE INITIALLY DEFERRED,
    "address_province_id" integer REFERENCES "sigia_province" ("id") DEFERRABLE INITIALLY DEFERRED,
    "address_canton_id" integer REFERENCES "sigia_canton" ("id") DEFERRABLE INITIALLY DEFERRED,
    "address_parish_id" integer REFERENCES "sigia_parish" ("id") DEFERRABLE INITIALLY DEFERRED,
    "marital_status" varchar(1),
    "address" text,
    "telephone" varchar(30),
    "cellphone" varchar(30),
    "handed_id_doc" boolean,
    "id_doc_img" varchar(100),
    "handed_voting_cert" boolean,
    "voting_cert_img" varchar(100),
    "handed_degree" boolean,
    "handed_degree_img" varchar(100),
    "handed_medical_cert" boolean,
    "medical_cert_img" varchar(100),
    "handed_birth_cert" boolean,
    "birth_cert_img" varchar(100),
    "disability" boolean,
    "disability_percent" integer NOT NULL,
    "disability_id" varchar(20),
    "ethnic_group_id" integer REFERENCES "sigia_ethnicgroup" ("id") DEFERRABLE INITIALLY DEFERRED,
    "email_confirmed" boolean
)
;
CREATE TABLE "sigia_teacher" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "institutional_email" varchar(75),
    "academic_category" varchar(30),
    "contract_type" varchar(2),
    "academic_unity" varchar(30),
    "hours_to_pedagogy" integer,
    "hours_to_research" integer,
    "hours_to_society" integer,
    "hours_to_other" integer,
    "other_activities" varchar(50),
    "studying" boolean NOT NULL
)
;
CREATE TABLE "sigia_charge" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "nombre" varchar(30) NOT NULL,
    "teacher_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "date_start_charge" time,
    "date_end_charge" time,
    "no_doc_charge" integer
)
;
CREATE TABLE "sigia_career" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "name" varchar(100) NOT NULL UNIQUE,
    "description" varchar(250) NOT NULL
)
;
CREATE TABLE "sigia_course" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "career_id" integer REFERENCES "sigia_career" ("id") DEFERRABLE INITIALLY DEFERRED,
    "description" varchar(30) NOT NULL,
    "type" varchar(1) NOT NULL,
    "period_id" integer NOT NULL REFERENCES "sigia_period" ("id") DEFERRABLE INITIALLY DEFERRED,
    "semester" varchar(1) NOT NULL,
    "level" integer NOT NULL,
    "parallel" varchar(1) NOT NULL,
    "max_quota" integer NOT NULL,
    "quota" integer NOT NULL,
    "payment_reg" double precision NOT NULL,
    "payment_ext" double precision NOT NULL,
    "payment_esp" double precision NOT NULL,
    "amount_payments" integer NOT NULL,
    "value_payments" integer NOT NULL,
    "applied_scholarship_from" integer NOT NULL
)
;
CREATE TABLE "sigia_matter" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "career_id" integer NOT NULL REFERENCES "sigia_career" ("id") DEFERRABLE INITIALLY DEFERRED,
    "description" varchar(30) NOT NULL,
    "period_id" integer NOT NULL REFERENCES "sigia_period" ("id") DEFERRABLE INITIALLY DEFERRED,
    "semester" varchar(1) NOT NULL,
    "level" integer NOT NULL,
    "parallel" varchar(1) NOT NULL,
    "credit" integer NOT NULL
)
;
CREATE TABLE "sigia_studies" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "teacher_id" integer NOT NULL REFERENCES "sigia_teacher" ("id") DEFERRABLE INITIALLY DEFERRED,
    "academic_level" integer NOT NULL,
    "institute" varchar(50) NOT NULL,
    "title" varchar(50) NOT NULL,
    "title_img" varchar(100) NOT NULL,
    "date_award" date NOT NULL,
    "country_id" integer NOT NULL REFERENCES "sigia_country" ("id") DEFERRABLE INITIALLY DEFERRED,
    "senescyt_id" varchar(200) NOT NULL
)
;
CREATE TABLE "sigia_student" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "career_id" integer REFERENCES "sigia_career" ("id") DEFERRABLE INITIALLY DEFERRED,
    "working" boolean,
    "company_name" varchar(100),
    "company_address" varchar(200),
    "charge" varchar(50),
    "work_telephone" varchar(50),
    "work_email" varchar(75),
    "campus_orig" varchar(50),
    "campus_city" varchar(50),
    "specialization" varchar(50),
    "language_know_lvl" varchar(1),
    "informatic_know_lvl" varchar(1),
    "income_sys" varchar(3),
    "first_time_ingress" date,
    "decline" boolean,
    "cohort" varchar(4),
    "date_graduation" date,
    "date_thesis_defense" date,
    "act_number" integer,
    "senescyt_number" integer
)
;
CREATE TABLE "sigia_studentnotes" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "student_id" integer NOT NULL REFERENCES "sigia_student" ("id") DEFERRABLE INITIALLY DEFERRED,
    "note" text NOT NULL
)
;
CREATE TABLE "sigia_bugreport" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "gravity" varchar(3) NOT NULL,
    "name" varchar(50) NOT NULL,
    "description" text NOT NULL,
    "snapshot" varchar(100),
    "state" varchar(1) NOT NULL
)
;
CREATE TABLE "sigia_enrollment" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "student_id" integer NOT NULL REFERENCES "sigia_student" ("id") DEFERRABLE INITIALLY DEFERRED,
    "course_id" integer NOT NULL REFERENCES "sigia_course" ("id") DEFERRABLE INITIALLY DEFERRED,
    "type" varchar(3) NOT NULL,
    "date" date NOT NULL,
    "financing_sys" varchar(4) NOT NULL,
    "condition" varchar(1) NOT NULL,
    "scholarship" integer NOT NULL,
    "payment_order_id" integer
)
;
CREATE TABLE "sigia_paymentorder" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "date_issue" date NOT NULL,
    "payout" boolean NOT NULL,
    "date_payment" date,
    "level" integer NOT NULL,
    "period_id" integer NOT NULL REFERENCES "sigia_period" ("id") DEFERRABLE INITIALLY DEFERRED,
    "semester" varchar(1) NOT NULL,
    "value" double precision NOT NULL,
    "payment_concept" varchar(4) NOT NULL,
    "number" integer NOT NULL,
    "enrollment_id" integer REFERENCES "sigia_enrollment" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
ALTER TABLE "sigia_enrollment" ADD CONSTRAINT "payment_order_id_refs_id_297712be" FOREIGN KEY ("payment_order_id") REFERENCES "sigia_paymentorder" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "sigia_contact" (
    "id" serial NOT NULL PRIMARY KEY,
    "created" timestamp with time zone NOT NULL,
    "modified" timestamp with time zone NOT NULL,
    "created_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "created_with_session_key" varchar(40),
    "modified_by_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "modified_with_session_key" varchar(40),
    "live" boolean,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "id_doc_num" varchar(30) NOT NULL,
    "email" varchar(75),
    "address" text,
    "telephone" varchar(30),
    "cellphone" varchar(30)
)
;
CREATE INDEX "sigia_period_created_by_id" ON "sigia_period" ("created_by_id");
CREATE INDEX "sigia_period_modified_by_id" ON "sigia_period" ("modified_by_id");
CREATE INDEX "sigia_period_name_like" ON "sigia_period" ("name" varchar_pattern_ops);
CREATE INDEX "sigia_period_predecessor_id" ON "sigia_period" ("predecessor_id");
CREATE INDEX "sigia_country_created_by_id" ON "sigia_country" ("created_by_id");
CREATE INDEX "sigia_country_modified_by_id" ON "sigia_country" ("modified_by_id");
CREATE INDEX "sigia_country_name_like" ON "sigia_country" ("name" varchar_pattern_ops);
CREATE INDEX "sigia_province_created_by_id" ON "sigia_province" ("created_by_id");
CREATE INDEX "sigia_province_modified_by_id" ON "sigia_province" ("modified_by_id");
CREATE INDEX "sigia_province_country_id" ON "sigia_province" ("country_id");
CREATE INDEX "sigia_canton_created_by_id" ON "sigia_canton" ("created_by_id");
CREATE INDEX "sigia_canton_modified_by_id" ON "sigia_canton" ("modified_by_id");
CREATE INDEX "sigia_canton_province_id" ON "sigia_canton" ("province_id");
CREATE INDEX "sigia_parish_created_by_id" ON "sigia_parish" ("created_by_id");
CREATE INDEX "sigia_parish_modified_by_id" ON "sigia_parish" ("modified_by_id");
CREATE INDEX "sigia_parish_canton_id" ON "sigia_parish" ("canton_id");
CREATE INDEX "sigia_ethnicgroup_created_by_id" ON "sigia_ethnicgroup" ("created_by_id");
CREATE INDEX "sigia_ethnicgroup_modified_by_id" ON "sigia_ethnicgroup" ("modified_by_id");
CREATE INDEX "sigia_institution_created_by_id" ON "sigia_institution" ("created_by_id");
CREATE INDEX "sigia_institution_modified_by_id" ON "sigia_institution" ("modified_by_id");
CREATE INDEX "sigia_userprofile_created_by_id" ON "sigia_userprofile" ("created_by_id");
CREATE INDEX "sigia_userprofile_modified_by_id" ON "sigia_userprofile" ("modified_by_id");
CREATE INDEX "sigia_userprofile_nationality_id" ON "sigia_userprofile" ("nationality_id");
CREATE INDEX "sigia_userprofile_birthplace_country_id" ON "sigia_userprofile" ("birthplace_country_id");
CREATE INDEX "sigia_userprofile_birthplace_province_id" ON "sigia_userprofile" ("birthplace_province_id");
CREATE INDEX "sigia_userprofile_birthplace_canton_id" ON "sigia_userprofile" ("birthplace_canton_id");
CREATE INDEX "sigia_userprofile_birthplace_parish_id" ON "sigia_userprofile" ("birthplace_parish_id");
CREATE INDEX "sigia_userprofile_address_province_id" ON "sigia_userprofile" ("address_province_id");
CREATE INDEX "sigia_userprofile_address_canton_id" ON "sigia_userprofile" ("address_canton_id");
CREATE INDEX "sigia_userprofile_address_parish_id" ON "sigia_userprofile" ("address_parish_id");
CREATE INDEX "sigia_userprofile_ethnic_group_id" ON "sigia_userprofile" ("ethnic_group_id");
CREATE INDEX "sigia_teacher_created_by_id" ON "sigia_teacher" ("created_by_id");
CREATE INDEX "sigia_teacher_modified_by_id" ON "sigia_teacher" ("modified_by_id");
CREATE INDEX "sigia_charge_created_by_id" ON "sigia_charge" ("created_by_id");
CREATE INDEX "sigia_charge_modified_by_id" ON "sigia_charge" ("modified_by_id");
CREATE INDEX "sigia_charge_teacher_id" ON "sigia_charge" ("teacher_id");
CREATE INDEX "sigia_career_created_by_id" ON "sigia_career" ("created_by_id");
CREATE INDEX "sigia_career_modified_by_id" ON "sigia_career" ("modified_by_id");
CREATE INDEX "sigia_career_name_like" ON "sigia_career" ("name" varchar_pattern_ops);
CREATE INDEX "sigia_course_created_by_id" ON "sigia_course" ("created_by_id");
CREATE INDEX "sigia_course_modified_by_id" ON "sigia_course" ("modified_by_id");
CREATE INDEX "sigia_course_career_id" ON "sigia_course" ("career_id");
CREATE INDEX "sigia_course_period_id" ON "sigia_course" ("period_id");
CREATE INDEX "sigia_matter_created_by_id" ON "sigia_matter" ("created_by_id");
CREATE INDEX "sigia_matter_modified_by_id" ON "sigia_matter" ("modified_by_id");
CREATE INDEX "sigia_matter_career_id" ON "sigia_matter" ("career_id");
CREATE INDEX "sigia_matter_period_id" ON "sigia_matter" ("period_id");
CREATE INDEX "sigia_studies_created_by_id" ON "sigia_studies" ("created_by_id");
CREATE INDEX "sigia_studies_modified_by_id" ON "sigia_studies" ("modified_by_id");
CREATE INDEX "sigia_studies_user_id" ON "sigia_studies" ("user_id");
CREATE INDEX "sigia_studies_teacher_id" ON "sigia_studies" ("teacher_id");
CREATE INDEX "sigia_studies_country_id" ON "sigia_studies" ("country_id");
CREATE INDEX "sigia_student_created_by_id" ON "sigia_student" ("created_by_id");
CREATE INDEX "sigia_student_modified_by_id" ON "sigia_student" ("modified_by_id");
CREATE INDEX "sigia_student_career_id" ON "sigia_student" ("career_id");
CREATE INDEX "sigia_studentnotes_created_by_id" ON "sigia_studentnotes" ("created_by_id");
CREATE INDEX "sigia_studentnotes_modified_by_id" ON "sigia_studentnotes" ("modified_by_id");
CREATE INDEX "sigia_studentnotes_student_id" ON "sigia_studentnotes" ("student_id");
CREATE INDEX "sigia_bugreport_created_by_id" ON "sigia_bugreport" ("created_by_id");
CREATE INDEX "sigia_bugreport_modified_by_id" ON "sigia_bugreport" ("modified_by_id");
CREATE INDEX "sigia_enrollment_created_by_id" ON "sigia_enrollment" ("created_by_id");
CREATE INDEX "sigia_enrollment_modified_by_id" ON "sigia_enrollment" ("modified_by_id");
CREATE INDEX "sigia_enrollment_student_id" ON "sigia_enrollment" ("student_id");
CREATE INDEX "sigia_enrollment_course_id" ON "sigia_enrollment" ("course_id");
CREATE INDEX "sigia_enrollment_payment_order_id" ON "sigia_enrollment" ("payment_order_id");
CREATE INDEX "sigia_paymentorder_created_by_id" ON "sigia_paymentorder" ("created_by_id");
CREATE INDEX "sigia_paymentorder_modified_by_id" ON "sigia_paymentorder" ("modified_by_id");
CREATE INDEX "sigia_paymentorder_user_id" ON "sigia_paymentorder" ("user_id");
CREATE INDEX "sigia_paymentorder_period_id" ON "sigia_paymentorder" ("period_id");
CREATE INDEX "sigia_paymentorder_enrollment_id" ON "sigia_paymentorder" ("enrollment_id");
CREATE INDEX "sigia_contact_created_by_id" ON "sigia_contact" ("created_by_id");
CREATE INDEX "sigia_contact_modified_by_id" ON "sigia_contact" ("modified_by_id");
CREATE INDEX "sigia_contact_user_id" ON "sigia_contact" ("user_id");

COMMIT;
