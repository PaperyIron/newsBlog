//Login.jsx
import React, { useState } from "react";
import LoginForm from "../components/loginform";
import SignupForm from "../components/signupForm";

function Login({onLogin}) {
    const [showLogin, setShowLogin] = useState("")

    return (
        <div>
        <h1>News Blog</h1>
        {showLogin ? (
            <>
                <LoginForm onLogin={onLogin} />
                <hr />
                <p>
                    Don't have an account? &nbsp;
                    <button onClick={() => setShowLogin(false)}>
                    Signup
                    </button>
                </p>
            </>
        ) : (
            <>
                <SignupForm onLogin={onLogin} />
                <hr />
                <p>
                Already have an account? &nbsp;
                <button onClick={() => setShowLogin(true)}>
                Login
                </button>
                </p>
            </>
        )}
        </div>
    )
}

export default Login;