import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "../pages/Login";
import Home from "../pages/Home";
import BlogDetail from "../pages/BlogDetail";
import BlogForm from "../pages/BlogForm";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkSession();
  }, []);

  function checkSession() {
    fetch("/server/check_session")
      .then((r) => {
        if (r.ok) {
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
  }

  function handleLogout() {
    setUser(null);
  }

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
          element={user ? <Home user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
        />
        
        <Route 
          path="/blogs/new" 
          element={user ? <BlogForm user={user} /> : <Navigate to="/login" />} 
        />
        
        <Route 
          path="/blogs/:id/edit" 
          element={user ? <BlogForm user={user} /> : <Navigate to="/login" />} 
        />
        
        <Route 
          path="/blogs/:id" 
          element={user ? <BlogDetail user={user} /> : <Navigate to="/login" />} 
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