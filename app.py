import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="Student Registration Portal", page_icon="🎓", layout="centered")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

DATA_FILE = "students.csv"


# ---------- Helper functions ----------
def is_valid_email(email):
    return "@" in email and "." in email.split("@")[-1] and " " not in email


def already_registered(rollno, username):
    try:
        with open(DATA_FILE) as f:
            for line in f.read().splitlines()[1:]:
                row = line.split(",")
                if row[9] == rollno or row[10] == username:
                    return True
    except FileNotFoundError:
        pass
    return False


def save_student(row):
    try:
        open(DATA_FILE).close()
        new_file = False
    except FileNotFoundError:
        new_file = True
    with open(DATA_FILE, "a") as f:
        if new_file:
            f.write("Name,Email,Phone,Age,Branch,Section,Year,DOB,Gender,Roll No,Username\n")
        f.write(",".join(str(x).replace(",", " ") for x in row) + "\n")


def chatbot_reply(message):
    msg = message.lower()
    if any(w in msg for w in ["hi", "hello", "hey"]):
        return "Hello! 👋 I'm the registration assistant. Ask me about the form."
    if "phone" in msg or "mobile" in msg:
        return "Enter a 10-digit phone number, digits only (e.g. 9876543210)."
    if "email" in msg:
        return "Use a valid email like name@example.com."
    if "password" in msg:
        return "Password must be at least 6 characters, and both password fields must match."
    if "roll" in msg:
        return "Enter your college roll number exactly as on your ID card."
    if "age" in msg:
        return "Age must be between 16 and 40."
    if "dob" in msg or "birth" in msg:
        return "Choose your day, month and year of birth from the dropdowns."
    if "branch" in msg or "section" in msg or "year" in msg:
        return "Pick your branch, section and year from the dropdown lists."
    if "username" in msg:
        return "Choose a unique username. It can't be reused by another student."
    if "submit" in msg or "register" in msg:
        return "Fill all fields correctly and click 'Submit'. Errors will show in red."
    if "bye" in msg or "thank" in msg:
        return "You're welcome! Good luck 🎓"
    return "Sorry, I didn't get that. Try asking about: name, email, phone, age, password, roll number or submit."


# ---------- Header ----------
st.markdown(
    """
    <div style="background:linear-gradient(135deg,#6d28d9,#c026d3 60%,#ec4899); padding:32px 20px;
                border-radius:18px; text-align:center; margin-bottom:28px;
                box-shadow:0 10px 30px rgba(168,85,247,0.35);">
        <h1 style="color:#ffffff; margin:0; padding:0; font-size:28px; font-weight:700; letter-spacing:1px;">
            🎓 STUDENT REGISTRATION PORTAL
        </h1>
        <h2 style="color:#f3e8ff; margin:12px 0 0 0; padding:0; font-size:18px; font-weight:500;">
            📝 Registration Portal
        </h2>
        <p style="color:#fbcfe8; margin:6px 0 0 0; font-size:14px;">
            Fill in your details
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Registration form ----------
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

with st.form("registration_form"):
    NAME = st.text_input("Enter your name:")
    EMAIL = st.text_input("Enter your email:")
    PHONE = st.text_input("Enter your phone number:", max_chars=10)
    AGE = st.number_input("Enter your age:", min_value=16, max_value=40, value=18, step=1)
    BRANCH = st.selectbox("Select your branch:", ["CSE", "AIML", "EC", "DS", "IT", "CS", "EEE"])
    SECTION = st.selectbox("Select your section:", ["A", "B", "C", "D", "E"])
    YEAR = st.selectbox("Select your year:", ["1st Year", "2nd Year", "3rd Year", "4th Year"])

    st.write("Enter your date of birth:")
    c1, c2, c3 = st.columns(3)
    DAY = c1.selectbox("Day", list(range(1, 32)))
    MONTH = c2.selectbox("Month", MONTHS)
    DOB_YEAR = c3.selectbox("Year", list(range(2012, 1979, -1)), index=7)

    GENDER = st.radio("Select your gender:", ["Male", "Female", "Other"], horizontal=True)
    ROLLNO = st.text_input("Enter your roll number:")
    USERNAME = st.text_input("Enter your username:")
    PASSWORD = st.text_input("Enter your password:", type="password")
    CONFIRM_PASSWORD = st.text_input("Confirm your password:", type="password")
    SUBMIT = st.form_submit_button("Submit")

# ---------- Validation ----------
if SUBMIT:
    errors = []

    if not all([NAME.strip(), EMAIL.strip(), PHONE.strip(), ROLLNO.strip(),
                USERNAME.strip(), PASSWORD, CONFIRM_PASSWORD]):
        errors.append("All fields are required.")
    else:
        if not is_valid_email(EMAIL.strip()):
            errors.append("Enter a valid email address.")
        if not (PHONE.isdigit() and len(PHONE) == 10):
            errors.append("Phone number must be exactly 10 digits.")
        if len(PASSWORD) < 6:
            errors.append("Password must be at least 6 characters.")
        if PASSWORD != CONFIRM_PASSWORD:
            errors.append("Passwords do not match.")
        if already_registered(ROLLNO.strip(), USERNAME.strip()):
            errors.append("Roll number or username is already registered.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        # Password is validated but not saved to the file (never store plain-text passwords)
        save_student([NAME.strip(), EMAIL.strip(), PHONE, AGE, BRANCH, SECTION, YEAR,
                      f"{DAY}-{MONTH}-{DOB_YEAR}", GENDER, ROLLNO.strip(), USERNAME.strip()])
        st.success(f"✅ Registration successful! Welcome, {NAME.strip()}.")
        st.balloons()

# ---------- Chatbot ----------
st.divider()
st.subheader("🤖 Need help? Ask the assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! 👋 Ask me anything about filling this form."}
    ]

chat_box = st.container(height=300)
with chat_box:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])

user_msg = st.chat_input("Type your question here...")
if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    st.session_state.messages.append({"role": "assistant", "content": chatbot_reply(user_msg)})
    st.rerun()