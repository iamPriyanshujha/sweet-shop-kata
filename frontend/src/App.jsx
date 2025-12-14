import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import SweetDashboard from './pages/SweetDashboard';
import Auth from './pages/Auth';

const App = () => {
    // Check local storage for token/user state on load
    const [user, setUser] = useState(() => {
        const token = localStorage.getItem('token');
        // Simple check: if token exists, user is authenticated
        if (token) {
            // NOTE: In a real app, you would decode the JWT to get user details/roles
            // Default to not admin unless explicitly set during login process
            return { isAuthenticated: true, isAdmin: false }; 
        }
        return null;
    });

    const handleLogin = (userData, token) => {
        // userData includes { isAuthenticated: true, isAdmin: bool, username: str }
        localStorage.setItem('token', token);
        // Ensure that the initial state is merged with new data if required
        setUser({ 
            isAuthenticated: true, 
            isAdmin: userData.isAdmin || false, 
            username: userData.username || 'user' 
        });
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        setUser(null);
    };

    return (
        <Router>
            <Header user={user} onLogout={handleLogout} />
            {/* The main content area */}
            <div className="container mt-4">
                <Routes>
                    {/* Publicly accessible route (Catalog/Dashboard) */}
                    <Route path="/" element={<SweetDashboard user={user} />} />
                    
                    {/* Auth route: Redirects to home if already logged in */}
                    <Route 
                        path="/auth" 
                        element={user ? <Navigate to="/" replace /> : <Auth onLogin={handleLogin} />} 
                    />
                    
                    {/* Protected Admin Route: Only accessible if logged in and admin */}
                    <Route path="/admin" element={
                        user && user.isAdmin 
                        ? <h2 className="text-danger">Admin Panel Placeholder</h2> 
                        : <Navigate to="/" replace />
                    }/>
                    
                    {/* Catch-all route, redirects to home */}
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;