from oil_palm_streamlit.authentication import Authentication
from oil_palm_streamlit.maps import show_map

import streamlit as st

auth = Authentication()
token, auth_status, username = auth.login()

if st.session_state["auth_status"]:
    auth.logout()
    show_map()
elif st.session_state["auth_status"] == False:
    st.error("Username/password is incorrect")
elif st.session_state["auth_status"] == None:
    st.warning("Please enter your username and password")
