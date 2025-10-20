"""
Simple authentication module for Streamlit
"""

import streamlit as st
import hashlib
import os
from typing import Dict, List

# User credentials (in production, store in database or environment variables)
USERS = {
    "admin": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",  # password
    "client1": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # client1
    "client2": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # client2
    "client3": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # client3
    "client4": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # client4
    "client5": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # client5
    "client6": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # client6
    "client7": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # client7
    "client8": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # client8
    "client9": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # client9
    "client10": "ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f",  # client10
}

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate user"""
    if username in USERS:
        hashed_password = hash_password(password)
        return USERS[username] == hashed_password
    return False

def login_form() -> bool:
    """Display login form and return authentication status"""
    st.markdown("## 🔐 Login Required")
    st.markdown("Please enter your credentials to access the Gap Analyzer.")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if authenticate_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
    
    return st.session_state.get("authenticated", False)

def logout():
    """Logout user"""
    if "authenticated" in st.session_state:
        del st.session_state.authenticated
    if "username" in st.session_state:
        del st.session_state.username
    st.rerun()

def require_auth():
    """Require authentication to access the app"""
    if not st.session_state.get("authenticated", False):
        login_form()
        return False
    return True

def show_user_info():
    """Show current user info"""
    if st.session_state.get("authenticated", False):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"👤 Logged in as: **{st.session_state.username}**")
        with col2:
            if st.button("🚪 Logout"):
                logout()
