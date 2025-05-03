import streamlit.components.v1 as components
from utils.cookies.cookieReader import cookieReader

# Set a cookie
def set_cookie(name, value, days=7):
    js = f"""
    <script>
    const date = new Date();
    date.setTime(date.getTime() + ({days}*24*60*60*1000));
    document.cookie = "{name}=" + encodeURIComponent("{value}") + "; expires=" + date.toUTCString() + "; path=/";
    </script>
    """
    return components.html(js, height=0)

# Get all cookies
def get_cookies():
    return cookieReader()

# Delete a cookie
def delete_cookie(name):
    return components.html(f"""
        <script>
            document.cookie = "{name}=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
        </script>
    """, height=0)
