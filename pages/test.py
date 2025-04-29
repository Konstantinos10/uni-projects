# test.py - A testing page for Streamlit navigation and features
import streamlit as st

st.set_page_config(
    page_title="Test Page",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    # Page header
    st.title("🧪 Testing Page")
    st.markdown("This page is for testing navigation and Streamlit components.")
    st.divider()
    
    # Section 1: Navigation test
    st.header("1. Navigation Test")
    st.markdown("Try these navigation options:")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔙 Go to Main Page (main.py)"):
            st.switch_page("main.py")
    with col2:
        if st.button("📚 Go to Learning Section"):
            st.switch_page("pages/1_📚_Εισαγωγή_στην_Python.py")
    
    st.divider()
    
    # Section 2: Component testing
    st.header("2. Streamlit Components Test")
    
    with st.expander("📋 Basic Components"):
        st.write("Text input:")
        name = st.text_input("Enter your name", "John Doe")
        
        st.write("Slider:")
        age = st.slider("Your age", 0, 100, 25)
        
        st.write("Checkbox:")
        agree = st.checkbox("I agree to terms")
        
        if st.button("Submit"):
            st.success(f"Submitted: {name}, {age} years old, Agreement: {agree}")
    
    with st.expander("📊 Data Display"):
        st.write("DataFrame:")
        import pandas as pd
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': ['a', 'b', 'c']
        })
        st.dataframe(df)
        
        st.write("Chart:")
        st.line_chart(df['A'])
    
    with st.expander("🎭 Session State"):
        if 'counter' not in st.session_state:
            st.session_state.counter = 0
            
        st.write("Current counter:", st.session_state.counter)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Increment"):
                st.session_state.counter += 1
                st.rerun()
        with col2:
            if st.button("Reset"):
                st.session_state.counter = 0
                st.rerun()
    
    st.divider()
    
    # Section 3: Debug information
    st.header("3. Debug Information")
    st.code(f"""
    Streamlit version: {st.__version__}
    Page: {__file__}
    """)

if __name__ == "__main__":
    main()