import React, { useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import Home from "./pages/Home";
import Medicines from "./pages/Medicines";
import Appointments from "./pages/Appointments";
import Prescriptions from "./pages/Prescriptions";
import { AppBar, Toolbar, Button, Container, Typography } from "@mui/material";
import "./styles/theme.css";

function App() {
  // Request notification permission on page load
  useEffect(() => {
    if ("Notification" in window) {
      Notification.requestPermission().then((permission) => {
        if (permission === "granted") {
          console.log("Notification permission granted.");
        }
      });
    }
  }, []);

  return (
    <Router>
      {/* Navigation Bar */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            MedBuddy
          </Typography>
          <Button color="inherit" component={Link} to="/">Home</Button>
          <Button color="inherit" component={Link} to="/medicines">Medicines</Button>
          <Button color="inherit" component={Link} to="/appointments">Appointments</Button>
          <Button color="inherit" component={Link} to="/prescriptions">Prescriptions</Button>
        </Toolbar>
      </AppBar>

      {/* Page Content */}
      <Container sx={{ mt: 4 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/medicines" element={<Medicines />} />
          <Route path="/appointments" element={<Appointments />} />
          <Route path="/prescriptions" element={<Prescriptions />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;
