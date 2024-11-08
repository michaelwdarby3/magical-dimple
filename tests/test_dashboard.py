import streamlit as st
from streamlit.testing import TestSession

def test_dashboard_loads():
    with TestSession() as session:
        session.run("dashboard/app.py")
        assert session.is_active()
