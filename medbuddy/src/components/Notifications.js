import { useEffect, useState } from "react";

const Notifications = () => {
    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8080");

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setNotifications((prev) => [...prev, `Time to take ${data.medicine} at ${data.time}`]);
        };

        return () => ws.close();
    }, []);

    return (
        <div className="notifications">
            {notifications.map((note, index) => (
                <p key={index}>{note}</p>
            ))}
        </div>
    );
};

export default Notifications;
