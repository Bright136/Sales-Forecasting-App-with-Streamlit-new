import streamlit as st

def set_theme():
    """
    Set the theme of the app.
    """
    theme = {
        'primaryColor': '#0078e7',
        'backgroundColor': '#f0f2f6',
        'secondaryBackgroundColor': '#ffffff',
        'textColor': '#1d1d1f',
        'font': 'sans-serif'
    }
    return theme
    # st.set_page_config(page_title='My App', page_icon=':chart_with_upwards_trend:', layout='wide', initial_sidebar_state='expanded', theme=theme)
