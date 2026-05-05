CREATE TYPE interview_type AS ENUM (
    'phone_screen',
    'coding',
    'system_design',
    'behavioral'
);

CREATE TYPE interview_status AS ENUM (
    'pending',
    'pass',
    'fail'
);

CREATE TABLE interviews (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    application_id INTEGER REFERENCES job_applications(id) NOT NULL,
    interview_type interview_type NOT NULL DEFAULT 'phone_screen',
    status interview_status NOT NULL,
    notes TEXT 
);