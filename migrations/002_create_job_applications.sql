CREATE TYPE application_status AS ENUM (
    'pending',
    'applied',
    'in_progress',
    'rejected',
    'offer'
);

CREATE TABLE job_applications (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    company_id INTEGER REFERENCES companies(id) NOT NULL,
    role_title VARCHAR(100),
    salary_min INT,
    salary_max INT,
    date_applied timestamptz NOT NULL DEFAULT NOW(), 
    status application_status NOT NULL DEFAULT 'pending',
    resume TEXT,
    cover_letter TEXT
);

COMMENT ON COLUMN job_applications.resume IS 'URL to S3 bucket containing resume';
COMMENT ON COLUMN job_applications.cover_letter IS 'URL to S3 bucket containing cover letter';