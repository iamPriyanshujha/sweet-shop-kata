import React from 'react';
import { Link } from 'react-router-dom';

const Header = ({ user, onLogout }) => {
    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div className="container">
                <Link className="navbar-brand" to="/">🍬 Sweet Shop Manager</Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        {user && user.isAdmin && (
                            <li className="nav-item">
                                <Link className="nav-link" to="/admin">Admin Tools</Link>
                            </li>
                        )}
                    </ul>
                    <div className="d-flex">
                        {user ? (
                            <>
                                <span className="navbar-text me-3 text-white">
                                    Logged In
                                </span>
                                <button className="btn btn-outline-light" onClick={onLogout}>
                                    Logout
                                </button>
                            </>
                        ) : (
                            <Link className="btn btn-outline-light" to="/auth">Login / Register</Link>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Header;