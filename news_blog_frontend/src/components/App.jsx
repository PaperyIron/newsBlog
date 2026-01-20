//App.jsx
import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "../pages/Login";
import Home from "../pages/Home";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/server/check_session")
      .then((r) => {
        if(r.ok) {
          r.json().then((user) => {
            setUser(user);
            setLoading(false);
          });
        } else {
          setLoading(false);
        }
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      <Routes>
        <Route 
          path="/login" 
          element={!user ? <Login onLogin={setUser} /> : <Navigate to="/" />} 
        />
        
        <Route 
          path="/" 
          element={user ? <Home user={user} /> : <Navigate to="/login" />} 
        />
        
        <Route 
          path="*" 
          element={<Navigate to={user ? "/" : "/login"} />} 
        />
      </Routes>
    </Router>
  );
}

export default App;