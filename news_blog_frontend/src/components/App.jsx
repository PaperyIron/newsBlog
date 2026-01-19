//App.jsx
import React, { useState, useEffect } from "react";
import Login from "../pages/Login";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch("/server/check_session").then((r) => {
      if(r.ok) {
        r.json().then((user) => setUser(user));
      }
    });
  }, []);

  if(!user) return <Login onLogin={setUser} />;

  return (
    <>
    <main>
      <p>You are logged in!</p>
    </main>
    </>
  );
}

export default App;