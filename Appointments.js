import React, { useState } from "react";
import { TextField, Button, List, ListItem, ListItemText, Container, Typography } from "@mui/material";
import { showNotification } from "../utils/notifications"; // Import Notification function
import "../styles/theme.css";

function Appointments() {
  const [appointment, setAppointment] = useState("");
  const [appointments, setAppointments] = useState([]);

  // Function to request notification permission
  const requestNotificationPermission = () => {
    if (Notification.permission !== "granted") {
      Notification.requestPermission().then((permission) => {
        if (permission === "granted") {
          console.log("✅ Notification permission granted.");
        } else {
          console.log("❌ Notification permission denied.");
        }
      });
    }
  };

  // Function to add appointment and trigger notification
  const addAppointment = () => {
    if (appointment.trim() !== "") {
      setAppointments([...appointments, appointment]);
      setAppointment("");

      // Show Notification for Appointment Alert
      showNotification("📅 Appointment Alert", `Your appointment with ${appointment} is scheduled.`);
    }
  };

  return (
    <Container>
      <Typography variant="h4">Doctor Appointment Manager</Typography>

      {/* Button to Enable Notifications */}
      <Button variant="contained" color="secondary" onClick={requestNotificationPermission} style={{ marginBottom: "10px" }}>
        Enable Notifications
      </Button>

      {/* Input Field for Appointment */}
      <TextField
        label="Doctor's Name & Time"
        variant="outlined"
        fullWidth
        value={appointment}
        onChange={(e) => setAppointment(e.target.value)}
        margin="normal"
      />

      {/* Add Appointment Button */}
      <Button variant="contained" color="primary" onClick={addAppointment}>
        Add Appointment
      </Button>

      {/* List of Appointments */}
      <List>
        {appointments.map((appt, index) => (
          <ListItem key={index}>
            <ListItemText primary={appt} />
          </ListItem>
        ))}
      </List>
    </Container>
  );
}

export default Appointments;
