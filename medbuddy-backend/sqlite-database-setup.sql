-- Create the users table
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the doctors table
CREATE TABLE doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Create the medicines table (reference table for medicine names)
CREATE TABLE medicines (
    medicine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Create the prescriptions table (links users to medicines)
CREATE TABLE prescriptions (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    medicine_id INTEGER NOT NULL,
    doses_per_day INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id)
);

-- Create the dosage_times table (stores specific times for each prescription)
CREATE TABLE dosage_times (
    dosage_time_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prescription_id INTEGER NOT NULL,
    time_of_day TIME NOT NULL,
    FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id)
);

-- Create indices for better query performance
CREATE INDEX idx_prescriptions_user_id ON prescriptions(user_id);
CREATE INDEX idx_dosage_times_prescription_id ON dosage_times(prescription_id);

CREATE TABLE dosage_tracking (
    tracking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    doses_taken INTEGER DEFAULT 1,
    total_doses_per_day INTEGER NOT NULL,
    intake_date DATE DEFAULT (date('now')),
    last_intake_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(medicine_id, user_id, intake_date)
);