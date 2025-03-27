import asyncio
import websockets
import sqlite3
from datetime import datetime, timedelta

class NotificationServer:
    def __init__(self, port=8080):
        self.port = port
        self.connections = set()
        self.db_path = 'medicine_reminder.db'

    async def send_medication_notifications(self, websocket, path):
        """
        Continuously check for medication notifications and send them via WebSocket
        """
        self.connections.add(websocket)
        try:
            while True:
                # Check for pending medication notifications
                notifications = self._get_pending_notifications()
                
                for notification in notifications:
                    # Send notification to the connected client
                    await websocket.send(json.dumps({
                        'medicine': notification['medicine_name'],
                        'time': notification['dosage_time'],
                        'user': notification['user_name']
                    }))
                
                # Wait for a few minutes before checking again
                await asyncio.sleep(300)  # Check every 5 minutes
        
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed")
        finally:
            self.connections.remove(websocket)

    def _get_pending_notifications(self):
        """
        Retrieve pending medication notifications from the database
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current time
            current_time = datetime.now().strftime('%H:%M')
            current_date = datetime.now().strftime('%Y-%m-%d')

            # Query to find upcoming medication doses
            cursor.execute('''
                SELECT 
                    u.name as user_name, 
                    m.name as medicine_name, 
                    dt.time_of_day as dosage_time
                FROM prescriptions p
                JOIN users u ON p.user_id = u.user_id
                JOIN medicines m ON p.medicine_id = m.medicine_id
                JOIN dosage_times dt ON p.prescription_id = dt.prescription_id
                LEFT JOIN dosage_tracking dt_track ON (
                    dt_track.medicine_id = m.medicine_id AND 
                    dt_track.user_id = u.user_id AND 
                    dt_track.intake_date = ?
                )
                WHERE 
                    dt.time_of_day = ? AND 
                    dt_track.tracking_id IS NULL
            ''', (current_date, current_time))

            notifications = [
                {
                    'user_name': row[0],
                    'medicine_name': row[1],
                    'dosage_time': row[2]
                } for row in cursor.fetchall()
            ]

            conn.close()
            return notifications

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    async def start_server(self):
        """
        Start the WebSocket server
        """
        server = await websockets.serve(
            self.send_medication_notifications, 
            "localhost", 
            self.port
        )
        print(f"WebSocket server started on ws://localhost:{self.port}")
        await server.wait_closed()

# Main entry point
async def main():
    notification_server = NotificationServer()
    await notification_server.start_server()

if __name__ == "__main__":
    import json
    import asyncio
    import websockets
    
    asyncio.run(main())
