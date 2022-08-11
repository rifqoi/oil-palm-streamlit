from oil_palm_streamlit.authentication import Authentication
from oil_palm_streamlit.database import Database
from sqlalchemy import inspect

auth = Authentication()
auth.login()
