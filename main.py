import streamlit as st

st.set_page_config(page_title="page title", layout="wide")

# Sidebar - User Profile & Navigation
with st.sidebar:
    st.title("page title")
    st.markdown("### Καλωσόρισες, Μαθητή!")
    st.markdown("#### Επίπεδο: Αρχάριος 🐣")
    st.markdown("---")
    section = st.radio("📚 Επιλογή Ενότητας:", [
        "Εισαγωγή στην Python",
        "Μεταβλητές & Τύποι",
        "If Statements",
        "Loops",
        "Συναρτήσεις",
        "Ασκήσεις Επανάληψης"
    ])
    st.markdown("---")
    st.markdown("🧠 Πρόοδος: 45%")

# Main Section - Learning Flow
st.title(f"📘 {section}")
st.markdown("#### Βήμα 1: Διάβασε το υλικό")

# Section Content
if section == "If Statements":
    st.markdown("""
    Οι **if δηλώσεις** επιτρέπουν στον κώδικά σου να παίρνει αποφάσεις!

    ```python
    x = 10
    if x > 5:
        print("Το x είναι μεγαλύτερο από 5!")
    ```
    """)

    # Practice Quiz
    st.markdown("#### Βήμα 2: Quiz")
    q1 = st.radio("Τι θα εμφανιστεί;", ["Τίποτα", "Το x είναι μεγαλύτερο από 5!", "Λάθος"])
    if st.button("✅ Έλεγχος"):
        if q1 == "Το x είναι μεγαλύτερο από 5!":
            st.success("Μπράβο! Σωστά! 🎉")
        else:
            st.error("Όχι ακριβώς! Δοκίμασε ξανά ή ζήτα βοήθεια από τον πράκτορα.")

    # Code Practice
    st.markdown("#### Βήμα 3: Γράψε Κώδικα")
    code = st.text_area("📝 Πληκτρολόγησε τον δικό σου κώδικα:", height=200)
    if st.button("🚀 Εκτέλεση"):
        with st.spinner("Εκτελείται..."):
            try:
                exec(code)
            except Exception as e:
                st.error(f"⚠️ Σφάλμα: {e}")

    # Help from AI Agent
    if st.button("🤖 Ζήτα βοήθεια από τον MentorAgent"):
        st.info("Ο MentorAgent λέει: 'Δοκίμασε να δεις αν το x είναι μικρότερο από 5 και χρησιμοποίησε else!'")
