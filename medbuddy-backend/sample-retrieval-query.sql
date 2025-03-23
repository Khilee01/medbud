SELECT 
    u.name AS patient_name,
    u.age AS patient_age,
    d.name AS doctor_name,
    m.name AS medicine_name,
    p.doses_per_day,
    GROUP_CONCAT(dt.time_of_day, ', ') AS dosage_times
FROM users u
JOIN prescriptions p ON u.user_id = p.user_id
JOIN doctors d ON p.doctor_id = d.doctor_id
JOIN medicines m ON p.medicine_id = m.medicine_id
JOIN dosage_times dt ON p.prescription_id = dt.prescription_id
WHERE u.user_id = 1
GROUP BY p.prescription_id
ORDER BY m.name;
