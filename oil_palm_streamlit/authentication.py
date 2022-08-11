import streamlit as st
import extra_streamlit_components as stx


class Authentication:
    def __init__(self):

        if "username" not in st.session_state:
            st.session_state["name"] = None
        if "auth_status" not in st.session_state:
            st.session_state["auth_status"] = None
        if "logout" not in st.session_state:
            st.session_state["logout"] = None
        self.cookie_manager = stx.CookieManager()

    def login(self):
        st.title("Oil Palm Detection")
        if st.session_state["auth_status"] is not True:
            login_form = st.form("Login")
            login_form.subheader("Login")

            self.username = login_form.text_input("Username").lower()
            self.password = login_form.text_input("Password", type="password")

            if login_form.write("[forgot password?](#login)"):
                st.write("check out this [link](%s)")

            if login_form.form_submit_button("Login"):
                st.write("cihuy")
