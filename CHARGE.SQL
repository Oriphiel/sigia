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