import streamlit as st
from streamlit.components.v1 import html



st.title("Κεφάλαια⭐")

# Define chapters
chapters = {
    "Κεφάλαιο 1": "chapter1",
    "Κεφάλαιο 2": "chapter2",
    "Κεφάλαιο 3": "chapter3",
    "Κεφάλαιο 4": "chapter4"
}

# Dropdown in main page
selected_chapter = st.selectbox(
    "Παρακάτω κεφάλαια:",
    options=list(chapters.keys()),
    index=0,
    key="chapter_select"
)


# Show selected chapter content
st.title(selected_chapter)

if selected_chapter == "Κεφάλαιο 1":
    st.write("Βασικές Έννοιες Python")
    st.button("1. Εκτυπωση κειμενου")
    st.button("2. Μεταβλητες")
    st.button("3. Απλες πραξεις")
    st.button("4. Είσοδος Δεδομένων")
    st.button("5. Σχόλια")
    st.button("6. Βασικές Συγκρίσεις")
elif selected_chapter == "Κεφάλαιο 2":
    st.write("Μεταβλητές και Τύποι Δεδομένων")
    st.button("1. Δημιουργία και Χρήση Μεταβλητών")
    st.button("2. Αντιστροφή Συμβολοσειράς")
    st.button("3. Τύποι Δεδομένων")
    st.button("4. Μετατροπή σε Ακέραιο (int)")
    st.button("5. Μετατροπή σε Πραγματικό (float)")
    st.button("6. Χρήση Boolean Τιμών")
    st.button("7. Σύνδεση Συμβολοσειρών με Μεταβλητές")
    st.button("8. Αριθμητικές Πράξεις με Μεταβλητές")
    st.button("9. Ενημέρωση Μεταβλητών")
    st.button("10. Λίστες ως Μεταβλητές")
elif selected_chapter == "Κεφάλαιο 3":
    st.write("Συνθήκες (if-else)")
    st.button("1. Βασική Συνθήκη (if)")
    st.button("2. Χρήση else")
    st.button("3. Χρήση elif")
    st.button("4. Συνθήκες με Είσοδο")
    st.button("5. Λογικές Πράξεις σε Συνθήκες")
    st.button("6. Χρήση or σε Συνθήκες")
    st.button("7. Έλεγχος Συμβολοσειράς")
    st.button("8. Ένθετες Συνθήκες")
    st.button("9. Έλεγχος Boolean Τιμών")
    st.button("10. Συνθήκες με Λίστες")
elif selected_chapter == "Κεφάλαιο 4":
    st.write("Βρόχοι (Loops)")
    st.button("1. Βασικός Βρόχος for με Range")
    st.button("2. Βρόχος for με Λίστα")
    st.button("3. Βασικός Βρόχος while")
    st.button("4. Βρόχος for με Βήμα (Step)")
    st.button("5. Χρήση break σε Βρόχο")
    st.button("6. Χρήση continue σε Βρόχο")
    st.button("7. Βρόχος με Είσοδο Χρήστη")
    st.button("8. Υπολογισμός Αθροίσματος με Βρόχο")
    st.button("9. Βρόχος για Επανάληψη Λίστας με Δείκτες")
    st.button("10. Ένθετοι Βρόχοι")
    st.button("11. Λίστα μέσα σε Λίστα (Nested Lists)")

st.markdown("""
<style>
    .stButton>button {
        width: 80%;
        padding: 10px;
        margin: 2px 0;
        background-color: #90EE90;  
        color: #000000; 
        border: 1px solid #76C776;
        transition: all 0.3s ease;  
    }
</style>
""", unsafe_allow_html=True)
