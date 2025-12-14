const API_BASE_URL = 'http://localhost:8000';

// Registers a new user (expects JSON body)
export const registerUser = (username, password) => {
    return fetch(`${API_BASE_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    });
};

// Login (expects URL-encoded form data body)
export const loginUser = (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    
    return fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
            // CRITICAL FIX: Must be form data for OAuth2PasswordRequestForm
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
    });
};

// Fetches sweets (requires Authorization header and will now hit the backend)
export const fetchSweets = (token) => {
    return fetch(`${API_BASE_URL}/api/sweets`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    });
};