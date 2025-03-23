-- Insert a user
INSERT INTO users (name, age) VALUES ('John Doe', 45);

-- Insert a doctor
INSERT INTO doctors (name) VALUES ('Dr. Smith');

-- Insert a medicine
INSERT INTO medicines (name) VALUES ('Lisinopril');

-- Insert a prescription
INSERT INTO prescriptions (user_id, doctor_id, medicine_id, doses_per_day)
VALUES (1, 1, 1, 2);

-- Insert dosage times for the prescription
INSERT INTO dosage_times (prescription_id, time_of_day)
VALUES (1, '08:00');

INSERT INTO dosage_times (prescription_id, time_of_day)
VALUES (1, '20:00');
