import React, { useEffect, useState } from "react";
import io from "socket.io-client";
import { showNotification } from "../utils/notifications";
import "../styles/theme.css";

const socket = io("http://localhost:5000"); // Connect to WebSocket server

function StockAlerts() {
  const [alert, setAlert] = useState("");

  useEffect(() => {
    socket.on("stock-alert", (message) => {
      setAlert(message);
      showNotification("Stock Alert", message);
    });

    return () => socket.off("stock-alert");
  }, []);

  return (
    <div className="container">
      <h2>Stock Alerts</h2>
      {alert && <p>{alert}</p>}
    </div>
  );
}

export default StockAlerts;
