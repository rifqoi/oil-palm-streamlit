from .config import settings

from datetime import datetime, timedelta

import streamlit as st
import requests
import extra_streamlit_components as stx
from captcha.image import ImageCaptcha
from jose import jwt


class Authentication:
    def __init__(self):

        if "username" not in st.session_state:
            st.session_state["username"] = None
        if "auth_status" not in st.session_state:
            st.session_state["auth_status"] = None
        if "token" not in st.session_state:
            st.session_state["token"] = None
        if "logout" not in st.session_state:
            st.session_state["logout"] = None

        self.cookie_name = settings.COOKIE_NAME
        self.cookie_expiry_days = settings.COOKIE_EXPIRY_DAYS
        self.api_url = settings.API_URL

        self.cookie_manager = stx.CookieManager()

    # def login(self):
    #     st.title("Oil Palm Detection")
    #     image = ImageCaptcha()
    #     if st.session_state["auth_status"] is not True:
    #         login_form = st.form("Login")
    #         login_form.subheader("Login")

    #         print("sebelum")
    #         data = image.generate("asd21312", format="png")
    #         print("sesudah")
    #         print()
    #         self.username = login_form.text_input("Username").lower()
    #         self.password = login_form.text_input("Password", type="password")
    #         login_form.image(data)
    #         self.captcha = login_form.text_input(
    #             "Input captcha",
    #         )

    #         if login_form.write("[forgot password?](#login)"):
    #             st.write("check out this [link](%s)")

    #         if login_form.form_submit_button("Login") and self.captcha == "asd1234":
    #             st.write("cihuy")

    def _jwt_decode(self):
        try:
            return jwt.decode(self.token, settings.JWT_SECRET, algorithms="HS256")
        except:
            return False

    def _check_cookies(self):
        self.token = self.cookie_manager.get(self.cookie_name)

        if self.token is not None:
            self.token = self._jwt_decode()

            if self.token is not False:
                if st.session_state["logout"] is not True:
                    if self.token["exp"] > datetime.utcnow().timestamp():
                        st.session_state["username"] = self.token["sub"]
                        st.session_state["auth_status"] = True

    def _check_credentials(self):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        request_body = {
            "username": self.username,
            "password": self.password,
        }
        response = requests.post(
            self.api_url,
            headers=headers,
            data=request_body,
        )

        if response.status_code == 200:
            payload = response.json()
            self.token = payload["access_token"]
            token_details = self._jwt_decode()
            username = token_details.get("sub")

            st.session_state["username"] = username
            st.session_state["token"] = response.json()["access_token"]
            st.session_state["auth_status"] = True

            self.cookie_manager.set(
                self.cookie_name,
                self.token,
                expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days),
            )
        else:
            st.session_state["auth_status"] = False

    def login(self):
        st.title("Oil Palm Detection")
        if st.session_state["auth_status"] is not True:
            self._check_cookies()
            if st.session_state["auth_status"] is not True:
                login_form = st.form("Login")
                login_form.subheader("Login")

                self.username = login_form.text_input("Username").lower()
                self.password = login_form.text_input("Password", type="password")

                if login_form.write("[forgot password?](#login)"):
                    st.write("check out this [link](%s)")

                login_form.write("[don't have user? register here!](?nav=/register)")

                if login_form.form_submit_button("Login"):
                    self._check_credentials()

        return (
            st.session_state["token"],
            st.session_state["auth_status"],
            st.session_state["username"],
        )

    def logout(self):
        if st.button("Logout"):
            self.cookie_manager.delete(self.cookie_name)
            st.session_state["logout"] = True
            st.session_state["name"] = None
            st.session_state["username"] = None
            st.session_state["auth_status"] = None
