import React, { useState } from "react";
import { TextField, Button, List, ListItem, ListItemText, Container, Typography } from "@mui/material";

function Prescriptions() {
  const [prescription, setPrescription] = useState("");
  const [prescriptions, setPrescriptions] = useState([]);

  const addPrescription = () => {
    if (prescription.trim() !== "") {
      setPrescriptions([...prescriptions, prescription]);
      setPrescription("");
    }
  };

  return (
    <Container>
      <Typography variant="h4">Prescription Storage</Typography>
      <TextField
        label="Upload Prescription Info"
        variant="outlined"
        fullWidth
        value={prescription}
        onChange={(e) => setPrescription(e.target.value)}
        margin="normal"
      />
      <Button variant="contained" color="primary" onClick={addPrescription}>
        Add Prescription
      </Button>
      <List>
        {prescriptions.map((pres, index) => (
          <ListItem key={index}>
            <ListItemText primary={pres} />
          </ListItem>
        ))}
      </List>
    </Container>
  );
}

export default Prescriptions;
