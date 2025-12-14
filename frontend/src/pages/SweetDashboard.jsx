import React, { useState, useEffect } from 'react';
import { fetchSweets } from '../services/api';

// No longer needs mockSweets defined here, as we will use the API

const SweetDashboard = ({ user }) => {
    const [sweets, setSweets] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    const loadSweets = async () => {
        setLoading(true);
        setError('');
        
        // Ensure user and token exist before fetching
        const token = localStorage.getItem('token');
        if (!token) {
            setError('User not authenticated. Please log in to view the full catalog.');
            setLoading(false);
            return;
        }

        try {
            // Fetch data from the new backend endpoint
            const response = await fetchSweets(token); 
            
            if (response.ok) {
                const data = await response.json();
                setSweets(data);
            } else if (response.status === 401) {
                setError('Authentication failed. Please log in again.');
            } else {
                setError(`Failed to fetch sweets: Status ${response.status}`);
            }
        } catch (err) {
            // Catch network errors
            setError('Network error: Could not connect to the API server.'); 
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadSweets();
    }, [user]); // Re-run if user status changes

    const handlePurchase = (sweetId) => {
        alert(`Purchasing sweet ${sweetId} - functionality coming soon!`);
    }

    const welcomeMessage = user && user.username ? `Welcome, ${user.username}!` : 'Sweet Shop Catalog';

    if (loading) return <div className="text-center mt-5">Loading Sweets...</div>;
    
    return (
        <div className="mt-5">
            <h1>🍭 {welcomeMessage}</h1>
            
            {/* Display error if present */}
            {error && <div className="alert alert-warning mt-3">{error}</div>}

            {sweets.length === 0 ? (
                <p className="mt-4">No sweets available in the catalog. Time to restock!</p>
            ) : (
                <div className="row">
                    {sweets.map(sweet => (
                        <div key={sweet.id} className="col-md-4 mb-4">
                            <div className="card h-100 shadow">
                                <div className="card-body">
                                    <h5 className="card-title">{sweet.name}</h5>
                                    <h6 className="card-subtitle mb-2 text-muted">{sweet.category}</h6>
                                    <p className="card-text">Price: ₹{sweet.price.toFixed(2)}</p>
                                    <p className="card-text">
                                        Stock: <span className={sweet.quantity > 0 ? 'text-success fw-bold' : 'text-danger fw-bold'}>
                                            {sweet.quantity} in stock
                                        </span>
                                    </p>
                                    <button 
                                        className="btn btn-success" 
                                        disabled={sweet.quantity === 0 || !user}
                                        onClick={() => handlePurchase(sweet.id)}
                                    >
                                        {sweet.quantity === 0 ? 'Out of Stock' : 'Purchase'}
                                    </button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default SweetDashboard;