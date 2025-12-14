import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { registerUser, loginUser } from '../services/api'; 

const Auth = ({ onLogin }) => {
    const [isLogin, setIsLogin] = useState(true);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const navigate = useNavigate();

    const switchMode = () => {
        setIsLogin(!isLogin);
        setError('');
        setSuccessMessage('');
    };

    const handleRegister = async () => {
        setError('');
        setSuccessMessage('');
        try {
            const response = await registerUser(username, password); 
            
            if (response.ok) {
                setSuccessMessage('Registration successful! Please log in.');
                setIsLogin(true); // Switch to login mode
            } else {
                const errorData = await response.json();
                
                // Robust error handling for Pydantic/FastAPI errors
                let errorMessage = 'Registration failed due to server error.';
                if (errorData.detail) {
                    if (Array.isArray(errorData.detail)) {
                        errorMessage = errorData.detail.map(d => `${d.loc.join('.')}: ${d.msg}`).join('; ');
                    } else if (typeof errorData.detail === 'string') {
                        errorMessage = errorData.detail;
                    }
                }
                setError(errorMessage);
            }
        } catch (err) {
            setError('Network error during registration. Check your server connection.');
        }
    };

    const handleLogin = async () => {
        setError('');
        setSuccessMessage('');
        
        try {
            // Use the dedicated service function which uses form data
            const response = await loginUser(username, password); 

            if (response.ok) {
                const data = await response.json();
                
                // NOTE: Passing basic user data
                onLogin({ isAuthenticated: true, username: username, isAdmin: false }, data.access_token);
                
                navigate('/'); // Redirect to the dashboard
            } else {
                const errorData = await response.json();
                
                // CRITICAL FIX: Ensure error is a simple string for rendering
                let errorMessage = 'Login failed.';
                if (errorData.detail) {
                    errorMessage = typeof errorData.detail === 'string' 
                        ? errorData.detail 
                        : 'Invalid username or password.'; // Default for 422/401
                }
                
                setError(errorMessage);
            }
        } catch (err) {
            setError('Network error during login. Check your server connection.');
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (isLogin) {
            handleLogin();
        } else {
            handleRegister();
        }
    };

    return (
        <div className="card shadow-sm p-4 mx-auto" style={{ maxWidth: '400px' }}>
            <h2 className="card-title text-center">{isLogin ? 'Login' : 'Register'}</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Username</label>
                    <input 
                        type="text" 
                        className="form-control" 
                        value={username} 
                        onChange={(e) => setUsername(e.target.value)} 
                        required 
                    />
                </div>
                <div className="mb-3">
                    <label className="form-label">Password</label>
                    <input 
                        type="password" 
                        className="form-control" 
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        required 
                    />
                </div>

                {/* ERROR FIX: Only render if error is a truthy string */}
                {error && typeof error === 'string' && <div className="alert alert-danger">{error}</div>}
                {successMessage && <div className="alert alert-success">{successMessage}</div>}

                <button type="submit" className="btn btn-primary w-100">
                    {isLogin ? 'Log In' : 'Register'}
                </button>
            </form>
            <div className="text-center mt-3">
                {isLogin ? (
                    <p>Don't have an account? <Link to="#" onClick={switchMode}>Register here</Link></p>
                ) : (
                    <p>Already have an account? <Link to="#" onClick={switchMode}>Login here</Link></p>
                )}
            </div>
        </div>
    );
};

export default Auth;