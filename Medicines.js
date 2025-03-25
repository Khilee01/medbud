import React, { useState } from "react";
import { TextField, Button, List, ListItem, ListItemText, Container, Typography } from "@mui/material";
import { showNotification } from "../utils/notifications"; // Import the function
import "../styles/theme.css";
import { Typography, Container } from "@mui/material";
function Medicines() {
  const [medicine, setMedicine] = useState("");
  const [medicines, setMedicines] = useState([]);

  // Function to request notification permission
  const requestNotificationPermission = () => {
    if (Notification.permission !== "granted") {
      Notification.requestPermission().then((permission) => {
        if (permission === "granted") {
          console.log("Notification permission granted.");
        }
      });
    }
  };

 
  
  function Medicines() {
    return (
      <Container>
        <Typography variant="h4">Medicines</Typography>
        <Typography variant="body1">Browse and order medicines online.</Typography>
      </Container>
    );
  }
  

  

  // Function to add medicine and show a reminder notification
  const addMedicine = () => {
    if (medicine.trim() !== "") {
      setMedicines([...medicines, medicine]);
      setMedicine("");

      // Show Notification for Reminder
      showNotification("Medicine Reminder", `Time to take ${medicine}!`);
    }
  };

  return (
    <Container>
      <Typography variant="h4">Medicine Tracker</Typography>
      <Button variant="contained" color="secondary" onClick={requestNotificationPermission}>
        Enable Notifications
      </Button>
      <TextField
        label="Medicine Name"
        variant="outlined"
        fullWidth
        value={medicine}
        onChange={(e) => setMedicine(e.target.value)}
        margin="normal"
      />
      <Button variant="contained" color="primary" onClick={addMedicine}>
        Add Medicine
      </Button>
      <List>
        {medicines.map((med, index) => (
          <ListItem key={index}>
            <ListItemText primary={med} />
          </ListItem>
        ))}
      </List>
    </Container>
  );
}

export default Medicines;
