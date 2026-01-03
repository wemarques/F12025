import yaml
import streamlit as st
from yaml.loader import SafeLoader
import os

def load_config(file_path):
    with open(file_path) as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

def check_login(username, password, config):
    """
    Verifica se o usuário e senha correspondem às credenciais no config.
    """
    credentials = config['credentials']['usernames']
    if username in credentials:
        if credentials[username]['password'] == password:
            return True
    return False

class Authenticator:
    def __init__(self, config_path):
        self.config = load_config(config_path)
        self.credentials = self.config['credentials']

    def login(self):
        st.sidebar.title("Login")
        
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
            
        if st.session_state['authentication_status']:
            return True
            
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Login"):
            if check_login(username, password, self.config):
                st.session_state['authentication_status'] = True
                st.session_state['name'] = self.credentials['usernames'][username]['name']
                st.session_state['username'] = username
                st.rerun()
            else:
                st.session_state['authentication_status'] = False
                st.error("Username/password is incorrect")
                
        return st.session_state['authentication_status']

    def logout(self):
        st.sidebar.button("Logout", on_click=self._reset_auth)

    def _reset_auth(self):
        st.session_state['authentication_status'] = None
        st.session_state['name'] = None
        st.session_state['username'] = None
