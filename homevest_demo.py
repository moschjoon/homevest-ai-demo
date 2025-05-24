if __name__ == "__main__":
    # --- Background Styling ---
    import streamlit as st
    from PIL import Image

    st.set_page_config(page_title="HomeVest AI Demo", layout="centered")

    page_bg_img = """
    <style>
    body {
    background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 50%, #f0abfc 100%);
    }
    [data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 50%, #f0abfc 100%);
    }
    [data-testid="stHeader"] {
    background: rgba(255,255,255,0);
    }
    [data-testid="stSidebar"] {
    background: #f3e8ff;
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # --- Logo ---
    try:
        logo = Image.open("logo.png")
        st.image(logo, width=180)
    except:
        st.caption("HomeVest AI")

    st.title("🏡 HomeVest AI – Smarter Homeownership Decisions")

    # --- Demo Info ---
    st.markdown("""
    > 🧪 **Demo only – powered by mock data**  
    > A working Streamlit-based MVP demo is already live and demonstrates:  
    > - ✅ Suburb Match  
    > - ✅ Grant Finder  
    > - ✅ Mortgage Optimiser  
    > - ✅ Equity Planner  
    > - ✅ Contract & Inspection Review  
    > - ✅ Tax Deduction  
    > - ✅ Broker Match  
    >
    > This prototype simulates key user flows and sets the foundation for full AI integration with OpenAI, OCR, and grant APIs under this grant.
    """, unsafe_allow_html=True)

    # --- Applicant Input ---
    st.header("👥 Applicant Details")
    with st.form("applicant_form"):
        joint = st.checkbox("Joint Application?")
        income1 = st.number_input("Primary Applicant Income ($)", 20000, 250000, 95000)
        income2 = st.number_input("Joint Applicant Income ($)", 20000, 250000, 75000) if joint else 0
        submitted = st.form_submit_button("Submit Applicant Details")
    total_income = income1 + income2
    st.write(f"Combined Household Income: ${total_income:,}")

    # --- 1. Suburb Match AI ---
    st.header("1. Suburb Match AI")
    goals = st.multiselect("Select top priorities:", ["Affordability", "Commute", "Safety", "Lifestyle", "Grants", "Growth"])
    if st.button("Find Matched Suburbs"):
        st.success("🏘️ Matches:\n- Blacktown\n- Parramatta\n- Auburn")

    # --- 2. Grant Finder AI ---
    st.header("2. Grant Finder")
    price = st.number_input("Target Property Price ($)", 100000, 1500000, 650000)
    first_home = st.radio("First Home?", ["Yes", "No"])
    if st.button("Check Eligibility"):
        if first_home == "Yes":
            st.info("Eligible: FHOG ($10,000) + Stamp Duty Waiver")
        else:
            st.warning("No major grants, but explore equity/tax opportunities.")

    # --- 3. Mortgage Optimiser ---
    st.header("3. Mortgage Optimiser")
    deposit = st.slider("Deposit %", 5, 40, 20)
    loan = price - (price * deposit / 100)
    payment = round((loan * 0.059) / 12, 2)
    st.write(f"Loan: ${loan:,.0f}")
    st.write(f"Monthly Repayment: ${payment:,.2f}")

    # --- 4. Equity Planner ---
    st.header("4. Equity Growth Planner")
    years = st.slider("Years to Project", 1, 10, 5)
    equity = round((loan * 0.03) * years + (price * deposit / 100))
    st.write(f"Equity in {years} years: ${equity:,}")
    st.caption("Tip: Add a granny flat or renovate to grow equity.")

    # --- 5. Property Evaluation Agent ---
    st.header("5. Contract & Inspection Review")
    st.file_uploader("Upload Contract/Inspection PDF", type=["pdf"])
    if st.button("Evaluate Property"):
        st.success("✅ Summary:\n- No major legal risks\n- Minor: drainage easement\n- Suggested Price: $635K–$665K")

    # --- 6. Tax Deduction Agent ---
    st.header("6. Tax Simulation")
    invest_mode = st.radio("How will you use the property?", ["Live in", "Rent out"])
    if invest_mode == "Rent out":
        st.write("Estimated tax deductions: $5,000/year")
    else:
        st.write("No tax benefit on owner-occupied homes.")

    # --- 7. Broker Match AI ---
    st.header("7. Broker Match")
    pref = st.radio("What's your priority?", ["Lowest rate", "Speed", "Ethical broker"])
    if st.button("Find Broker"):
        st.success("Best Match: SmartFinance – 2.89% fixed – 5-day approval")

    # --- Export Button ---
    st.button("📄 Export Smart Buyer Report")

    # --- Footer ---
    st.markdown("""
    ---  
    🔒 *This MVP is a prototype created for NSW MVP Grant review. All insights are simulated to showcase planned functionality. Full AI + data integrations will follow grant-supported build.*
    """)
