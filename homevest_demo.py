import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="HomeVest AI – Grant Demo", layout="wide", page_icon="🏡")

# --- Custom Styling ---
custom_style = '''
<style>
body {
    background: linear-gradient(135deg, #f0f4ff, #f5ecff);
    font-family: 'Segoe UI', sans-serif;
}
[data-testid="stAppViewContainer"] > .main {
    background: linear-gradient(120deg, #ffffff 30%, #eef2ff 100%);
    padding: 2rem;
}
h1, h2, h3, h4 {
    color: #3b0764;
}
.stButton button {
    background-color: #7c3aed;
    color: white;
    border-radius: 0.5rem;
}
.stButton button:hover {
    background-color: #6b21a8;
}
</style>
'''
st.markdown(custom_style, unsafe_allow_html=True)

# --- Header ---
col1, col2 = st.columns([1, 5])
with col1:
    try:
        logo = Image.open("logo.png")
        st.image(logo, width=120)
    except:
        st.write("🏡")

with col2:
    st.title("HomeVest AI")
    st.caption("Your AI-powered property journey – from grant matching to equity planning")

st.markdown("#### 🧪 *NSW MVP Grant Demo – mock data prototype*")
st.info("This app simulates the full user journey with mock data. It includes agents for suburb match, grant discovery, climate risk, mortgage simulation, contract review, tax deduction, and broker match.")

# --- 1. Applicant Setup ---
st.header("👥 1. Applicant Setup")
app_type = st.selectbox("Application Type", ["Single", "Joint", "Multiple"])
col1, col2 = st.columns(2)
with col1:
    income = st.number_input("Primary Income ($)", 20000, 300000, 95000)
    if app_type != "Single":
        joint_income = st.number_input("Joint Applicant(s) Income ($)", 20000, 300000, 75000)
    else:
        joint_income = 0
    total_income = income + joint_income
with col2:
    super_bal = st.number_input("Superannuation Balance ($)", 1000, 200000, 30000)
    first_home = st.radio("Is this your first home?", ["Yes", "No"])
st.success(f"Total Income: ${total_income:,.0f}")
if first_home == "Yes" and super_bal > 5000:
    st.info("✅ Likely eligible for **First Home Super Saver (FHSS)** scheme")

# --- 2. Suburb Match + Climate ---
st.header("📍 2. Suburb Match + Climate Risk")
prefs = st.multiselect("Choose top 3 preferences", ["Affordability", "Commute", "Grants Access", "Safety", "Low Climate Risk", "Growth Potential"])
if st.button("🎯 Get Suburb Matches"):
    st.success("🏘️ Top Matches:")
    st.markdown("""
- **Blacktown** – Affordable, FHOG, low flood risk  
- **Parramatta** – Lively hub, mid-risk zone, FHSS eligible  
- **Auburn** – Fast growth, climate safe, price uplift potential
""")

# --- 3. Grants & FHSS ---
st.header("🎁 3. Grant + Scheme Matching")
prop_price = st.slider("Target Property Price ($)", 300000, 1500000, 700000, step=50000)
if st.button("🔍 Check Eligibility"):
    st.subheader("You may be eligible for:")
    st.markdown("""
- ✅ **FHOG** ($10,000)  
- ✅ **Stamp Duty Waiver**  
- ✅ **FHSS** – Release up to $50,000 from super  
- ✅ **Solar & Green Home Rebate**
""")

# --- 4. Mortgage Simulation ---
st.header("💸 4. Mortgage Simulation")
rba_rate = 4.35
use_custom = st.checkbox("Manually override total interest rate?")
if use_custom:
    custom_rate = st.slider("Custom Interest Rate (%)", 2.0, 10.0, 5.89)
    rate_used = custom_rate
else:
    margin = st.slider("Estimated Bank Margin (%)", 1.0, 3.5, 2.5)
    rate_used = rba_rate + margin
    st.caption(f"🏦 Based on RBA rate ({rba_rate}%) + bank margin ({margin}%)")

deposit_pct = st.slider("Deposit (%)", 5, 40, 20)
deposit_amt = prop_price * deposit_pct / 100
loan_amt = prop_price - deposit_amt
monthly = (loan_amt * rate_used / 100) / 12

col1, col2 = st.columns(2)
with col1:
    st.metric("Loan Estimate", f"${loan_amt:,.0f}")
with col2:
    st.metric("Monthly Repayment", f"${monthly:,.2f}")

# --- 5. Equity Forecast ---
st.header("📈 5. Equity & ROI Planner")
years = st.slider("Years Forecast", 1, 15, 5)
growth_rate = random.uniform(2.5, 4.5)
equity = round((loan_amt * (growth_rate / 100)) * years + deposit_amt)
st.success(f"Projected Equity in {years} years: ${equity:,.0f}")
st.caption("💡 Tip: Granny flat or solar upgrade can improve ROI.")

# --- 6. Tax Deduction ---
st.header("🧾 6. Tax Deduction Analysis")
tax_mode = st.radio("Choose Analysis Type", ["Forecast Future (Rentvesting)", "Current Year Report (Manual Entry)"])
if tax_mode == "Forecast Future (Rentvesting)":
    rent_years = st.slider("Years Renting the Property", 1, 15, 5)
    annual_deduction = 6200
    future_total = annual_deduction * rent_years
    st.success(f"📈 Estimated total deductions over {rent_years} years: ${future_total:,}")
else:
    interest = st.number_input("Loan Interest Paid ($)", 0, 50000, 12000)
    repairs = st.number_input("Repairs & Maintenance ($)", 0, 10000, 1500)
    depreciation = st.number_input("Depreciation Allowance ($)", 0, 8000, 2200)
    agent_fees = st.number_input("Agent/Management Fees ($)", 0, 10000, 1800)
    other_costs = st.number_input("Other Allowable Costs ($)", 0, 10000, 500)
    total_deductions = interest + repairs + depreciation + agent_fees + other_costs
    st.success(f"🧾 Your current tax deduction total: ${total_deductions:,.0f}")

# --- 7. Contract & Inspection Review ---
st.header("📜 7. Contract & Inspection Check")
st.file_uploader("Upload Contract or Inspection PDF", type=["pdf"])
if st.button("⚖️ Run Check"):
    issues = ["Minor guttering issue", "Drainage easement", "Moderate traffic noise"]
    suggestion = random.choice([
        "Consider offer with $10K reduction",
        "Get structural inspection before proceeding",
        "Negotiate maintenance clauses"
    ])
    st.error("⚠️ Issues Detected:")
    st.write(f"- {random.choice(issues)}\n- {random.choice(issues)}")
    st.warning(f"💬 Suggestion: {suggestion}")

# --- 8. Broker Match AI ---
st.header("🔍 8. Broker Match AI")
broker_goal = st.selectbox("Broker preference", ["Lowest Rate", "Ethical Advice", "Fast Approval"])
if st.button("🎯 Find Broker"):
    brokers = {
        "Lowest Rate": "SmartFinance Co. – 2.79% fixed, approval in 4 days",
        "Ethical Advice": "GreenHome Brokers – 2.99%, solar loan certified",
        "Fast Approval": "QuickMortgage – 3.05%, pre-approval in 24h"
    }
    st.success(f"📨 Recommended Broker: {brokers[broker_goal]}")

# --- 9. Inspector Finder ---
st.header("🕵️ 9. Inspector Finder")
location = st.text_input("Property Suburb or Postcode")
inspection_type = st.selectbox("Inspection Type", ["Building Only", "Pest Only", "Building & Pest"])
urgency = st.radio("Urgency Level", ["Standard (1 week)", "Express (48h)"])
if st.button("🔎 Find Inspectors"):
    st.success("👷 2 Inspectors Found Nearby:")
    st.markdown("""
- **SafeHome Inspections** – 4.9⭐ | $450 | Available: 2 days  
- **NSW Property Checks** – 4.7⭐ | $390 | Available: 5 days  
""")

# --- 10. Home Insurance Advisor ---
st.header("🛡️ 10. Home Insurance Match")
structure_type = st.selectbox("Building Type", ["House", "Apartment", "Townhouse"])
contents_cover = st.checkbox("Include contents insurance?")
esg_score = st.slider("Climate Risk (0 = low risk, 10 = high risk)", 0, 10, 3)
if st.button("🏠 Recommend Insurance"):
    st.success("✅ Top Home Insurance Policies:")
    st.markdown(f"""
- **SureCover Basic** – ${round(1300 + esg_score * 40)}/yr  
- **GreenGuard Premium** – ${round(1500 + esg_score * 30)}/yr – includes solar & ESG add-ons
""")

# --- Export ---
st.button("📄 Export Smart Buyer PDF Report")
st.markdown("---")
st.caption("🔐 Mock simulation for NSW MVP Grant – All data is illustrative and educational.")
