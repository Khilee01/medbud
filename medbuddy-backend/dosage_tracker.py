import sqlite3
from datetime import datetime, timedelta

class DosageTracker:
    def __init__(self, user_name, medicine_name):
        """
        Initialize the DosageTracker with user and medicine information.
        
        Args:
            user_name (str): Name of the user
            medicine_name (str): Name of the medicine
        """
        self.DB_PATH = 'medicine_reminder.db'
        self.user_name = user_name
        self.medicine_name = medicine_name

    def _get_user_id(self, cursor):
        """
        Retrieve user ID from the database.
        
        Args:
            cursor (sqlite3.Cursor): Database cursor
        
        Returns:
            int or None: User ID if found, None otherwise
        """
        cursor.execute('SELECT user_id FROM users WHERE name = ?', (self.user_name,))
        user_result = cursor.fetchone()
        return user_result[0] if user_result else None

    def _get_medicine_id(self, cursor):
        """
        Retrieve medicine ID from the database.
        
        Args:
            cursor (sqlite3.Cursor): Database cursor
        
        Returns:
            int or None: Medicine ID if found, None otherwise
        """
        cursor.execute('SELECT medicine_id FROM medicines WHERE name = ?', (self.medicine_name,))
        medicine_result = cursor.fetchone()
        return medicine_result[0] if medicine_result else None

    def get_medication_details(self):
        """
        Retrieve comprehensive medication details for the specific user and medication.
        
        Returns:
            dict: Medication details including dosage information
        """
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()

            # Get user ID and medicine ID
            user_id = self._get_user_id(cursor)
            if not user_id:
                conn.close()
                return None

            medicine_id = self._get_medicine_id(cursor)
            if not medicine_id:
                conn.close()
                return None

            # Fetch comprehensive medication details
            cursor.execute('''
                SELECT 
                    m.medicine_id, 
                    p.doses_per_day, 
                    dt.dosage_time_id,
                    dt.time_of_day,
                    (SELECT COUNT(*) FROM dosage_tracking 
                     WHERE medicine_id = m.medicine_id 
                     AND user_id = ? 
                     AND intake_date = date('now')) as doses_taken,
                    (SELECT MIN(last_intake_time) FROM dosage_tracking 
                     WHERE medicine_id = m.medicine_id 
                     AND user_id = ? 
                     AND intake_date = date('now')) as first_intake_time
                FROM medicines m
                JOIN prescriptions p ON m.medicine_id = p.medicine_id
                JOIN dosage_times dt ON p.prescription_id = dt.prescription_id
                WHERE m.medicine_id = ? AND p.user_id = ?
                GROUP BY m.medicine_id, dt.time_of_day
            ''', (user_id, user_id, medicine_id, user_id))

            results = cursor.fetchall()
            conn.close()

            if not results:
                return None

            # Organize results
            return {
                'medicine_id': results[0][0],
                'total_doses': results[0][1],
                'dosage_times': [result[3] for result in results],
                'doses_taken': results[0][4],
                'first_intake_time': results[0][5]
            }

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def track_dosage(self):
        """
        Track and record medication dosage with advanced validation.
        
        Returns:
            dict: Dosage tracking status and details
        """
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()

            # Get user and medicine IDs
            user_id = self._get_user_id(cursor)
            if not user_id:
                conn.close()
                return {'status': 'error', 'message': 'User not found'}

            medicine_id = self._get_medicine_id(cursor)
            if not medicine_id:
                conn.close()
                return {'status': 'error', 'message': 'Medicine not found'}

            # Get medication details
            medication_details = self.get_medication_details()
            if not medication_details:
                conn.close()
                return {'status': 'error', 'message': 'Medication details not found'}

            total_doses = medication_details['total_doses']
            doses_taken = medication_details['doses_taken']
            dosage_times = medication_details['dosage_times']
            current_time = datetime.now()
            current_time_str = current_time.strftime('%H:%M')

            # Check if maximum daily doses reached
            if doses_taken >= total_doses:
                conn.close()
                return {
                    'status': 'max_dose_reached',
                    'message': 'Maximum daily dosage reached. Do not take more medication.',
                    'doses_taken': doses_taken,
                    'total_doses': total_doses
                }

            # Validate current time against prescribed dosage times
            valid_intake = any(
                abs(
                    (datetime.strptime(current_time_str, '%H:%M') - datetime.strptime(dose_time, '%H:%M')).total_seconds()
                ) < 1800  # Within 30 minutes of prescribed time
                for dose_time in dosage_times
            )

            if not valid_intake:
                conn.close()
                return {
                    'status': 'wrong_time',
                    'message': f'Not the right time to take medication. Prescribed times: {", ".join(dosage_times)}',
                    'prescribed_times': dosage_times
                }

            # Record the dosage
            cursor.execute('''
                INSERT INTO dosage_tracking 
                (medicine_id, user_id, doses_taken, total_doses_per_day, intake_date, last_intake_time)
                VALUES (?, ?, ?, ?, date('now'), datetime('now'))
            ''', (medicine_id, user_id, doses_taken + 1, total_doses))

            conn.commit()
            conn.close()

            # Determine next dosage time
            next_dosage_times = [
                time for time in dosage_times 
                if datetime.strptime(time, '%H:%M') > current_time.time()
            ]

            return {
                'status': 'dosage_tracked',
                'doses_taken': doses_taken + 1,
                'total_doses': total_doses,
                'current_time': current_time_str,
                'next_dosage_times': next_dosage_times,
                'message': f'Dosage taken. {doses_taken + 1} of {total_doses} doses taken today.'
            }

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {
                'status': 'error',
                'message': f'Database error: {e}'
            }

    def get_dose_history(self, days=7):
        """
        Retrieve dose history for the specified medicine and user.
        
        Args:
            days (int): Number of previous days to retrieve history for
        
        Returns:
            list: List of dose tracking records
        """
        try:
            conn = sqlite3.connect(self.DB_PATH)
            cursor = conn.cursor()

            user_id = self._get_user_id(cursor)
            medicine_id = self._get_medicine_id(cursor)

            if not user_id or not medicine_id:
                conn.close()
                return []

            # Retrieve dose history for the specified number of days
            cursor.execute('''
                SELECT intake_date, doses_taken, total_doses_per_day, last_intake_time
                FROM dosage_tracking
                WHERE medicine_id = ? AND user_id = ?
                AND intake_date >= date('now', ?)
                ORDER BY intake_date DESC
            ''', (medicine_id, user_id, f'-{days} days'))

            # Convert results to a list of dictionaries
            history = [
                {
                    'date': row[0],
                    'doses_taken': row[1],
                    'total_doses': row[2],
                    'last_intake_time': row[3]
                } for row in cursor.fetchall()
            ]

            conn.close()
            return history

        except sqlite3.Error as e:
            print(f"Dose history retrieval error: {e}")
            return []

# Example usage demonstration
def main():
    # Example: Tracking dose for a user's specific medicine
    tracker = DosageTracker('John Doe', 'Aspirin')
    
    # Get medication details
    details = tracker.get_medication_details()
    print("Medication Details:", details)
    
    # Track a dose
    result = tracker.track_dosage()
    print("Dosage Tracking Result:", result)
    
    # Get dose history
    history = tracker.get_dose_history()
    print("Dose History:", history)

if __name__ == "__main__":
    main()