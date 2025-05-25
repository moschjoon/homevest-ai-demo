import streamlit as st
from PIL import Image
import random
import plotly.graph_objects as go

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

# --- 6. Smart Property Portfolio Planner ---
st.header("🏘️ 6. Smart Property Portfolio Planner")

goal_props = st.number_input("🎯 Desired Number of Properties", min_value=1, max_value=10, value=3)
years_to_target = st.slider("⏳ Years to Reach Goal", 3, 30, 10)
salary_growth = st.slider("📈 Annual Salary Growth (%)", 0.0, 10.0, 3.0)

st.markdown("The planner forecasts how you can reach your goal by suggesting locations and property types based on price, equity, and lending criteria.")

# Mock property market data (location + price ranges)
market_data = {
    "Blacktown": {"House": 750000, "Unit": 580000},
    "Parramatta": {"Unit": 720000, "Townhouse": 820000},
    "Auburn": {"Unit": 630000, "House": 790000},
    "Penrith": {"House": 670000, "Unit": 520000},
    "Liverpool": {"Townhouse": 680000, "Unit": 560000},
}

# Lending assumptions
buffer_rate = 0.08  # Stress-tested interest rate
repayment_limit = 0.35
min_equity_pct = 0.20  # 20% deposit
growth_rate = 0.03

# Starting state
current_salary = income + joint_income
current_equity = equity
portfolio = 1
suggestions = []

# --- Occupancy Preference ---
occupancy = st.radio("🏠 Occupancy Goal for Future Properties", ["Live in", "Rentvest"])

# Custom market preferences based on strategy
preferred_suburbs_livein = ["Parramatta", "Blacktown", "Liverpool"]
preferred_suburbs_rentvest = ["Penrith", "Auburn", "Blacktown"]

if occupancy == "Live in":
    suburb_filter = preferred_suburbs_livein
    st.caption("Focusing on areas with strong amenities and schools.")
else:
    suburb_filter = preferred_suburbs_rentvest
    st.caption("Focusing on high-growth or high-yield rentvestment suburbs.")

# Forecast loop by year
for year in range(1, years_to_target + 1):
    current_salary *= (1 + salary_growth / 100)
    current_equity += 50000  # Simulated annual equity growth

    viable_options = []
    for suburb, types in market_data.items():
        if suburb not in suburb_filter:
            continue
        for prop_type, price in types.items():
            repayment_ratio = (loan_amt * buffer_rate) / current_salary
            if current_equity >= price * min_equity_pct and repayment_ratio <= repayment_limit:
                viable_options.append((price, suburb, prop_type))

    viable_options.sort()  # Lowest price first
    if viable_options and portfolio < goal_props:
        selected = viable_options[0]
        price, suburb, prop_type = selected
        current_equity -= price * min_equity_pct
        suggestions.append(
            f"📍 Year {year}: Buy a **{prop_type} in {suburb}** for ${price:,} – using equity ${round(price * 0.2):,}"
        )
        portfolio += 1
    else:
        suggestions.append(f"📍 Year {year}: Hold & build equity – not yet enough to buy")

# Output
st.subheader("📆 Forecast Plan")
for s in suggestions:
    st.markdown(s)

# --- Portfolio Line Chart ---
st.subheader("📊 Portfolio Growth Chart")

years_list = list(range(1, years_to_target + 1))
prop_counts = []
equity_track = []
curr_salary = income + joint_income
curr_equity = equity
curr_portfolio = 1

for year in years_list:
    curr_salary *= (1 + salary_growth / 100)
    curr_equity += 50000
    viable_found = False
    for suburb in suburb_filter:
        for prop_type, price in market_data.get(suburb, {}).items():
            if curr_equity >= price * min_equity_pct and ((loan_amt * buffer_rate) / curr_salary) <= repayment_limit:
                curr_equity -= price * min_equity_pct
                curr_portfolio += 1
                viable_found = True
                break
        if viable_found:
            break
    prop_counts.append(curr_portfolio)
    equity_track.append(curr_equity)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=years_list, y=prop_counts,
    name="Total Properties",
    mode="lines+markers",
    line=dict(color="#636EFA", width=3),
    marker=dict(size=8, symbol="circle"),
    hovertemplate="Year %{x}: %{y} properties"
))

fig.add_trace(go.Scatter(
    x=years_list, y=equity_track,
    name="Equity ($)",
    mode="lines+markers",
    yaxis="y2",
    line=dict(color="#00CC96", width=3, dash="dash"),
    marker=dict(size=8, symbol="diamond"),
    hovertemplate="Year %{x}: $%{y:,.0f} equity"
))

fig.update_layout(
    title=dict(
        text="📈 Property Count and Equity Forecast",
        font=dict(size=22, color="#3b0764"),
        x=0.5
    ),
    xaxis=dict(
        title="Year",
        showgrid=True,
        gridcolor="#e5ecf6",
        tickmode="linear"
    ),
    yaxis=dict(
        title="Properties",
        side="left",
        showgrid=True,
        gridcolor="#e5ecf6",
        rangemode="tozero"
    ),
    yaxis2=dict(
        title="Equity ($)",
        overlaying='y',
        side='right',
        showgrid=False,
        tickformat=",.0f",
        rangemode="tozero"
    ),
    legend=dict(
        x=0.5, y=1.15, orientation="h", xanchor="center",
        bgcolor="rgba(255,255,255,0.7)", bordercolor="#ccc", borderwidth=1
    ),
    plot_bgcolor="#fcfcff",
    paper_bgcolor="#f7f7fa",
    height=450,
    margin=dict(t=80, b=40, l=60, r=60)
)

st.plotly_chart(fig, use_container_width=True)

if portfolio >= goal_props:
    st.success(f"🎉 Based on equity + affordability, you may own {goal_props} properties in {year} years!")
else:
    st.warning("⚠️ Timeline may need to extend — not enough equity/income for desired growth.")


# --- 7. Tax Deduction ---
st.header("🧾 7. Tax Deduction Analysis")
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

# --- 8. Contract & Inspection Review ---
st.header("📜 8. Contract & Inspection Check")
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

# --- 9. Broker Match AI ---
st.header("🔍 9. Broker Match AI")
broker_goal = st.selectbox("Broker preference", ["Lowest Rate", "Ethical Advice", "Fast Approval"])
if st.button("🎯 Find Broker"):
    brokers = {
        "Lowest Rate": "SmartFinance Co. – 2.79% fixed, approval in 4 days",
        "Ethical Advice": "GreenHome Brokers – 2.99%, solar loan certified",
        "Fast Approval": "QuickMortgage – 3.05%, pre-approval in 24h"
    }
    st.success(f"📨 Recommended Broker: {brokers[broker_goal]}")

# --- 10. Inspector Finder ---
st.header("🕵️ 10. Inspector Finder")
location = st.text_input("Property Suburb or Postcode")
inspection_type = st.selectbox("Inspection Type", ["Building Only", "Pest Only", "Building & Pest"])
urgency = st.radio("Urgency Level", ["Standard (1 week)", "Express (48h)"])
if st.button("🔎 Find Inspectors"):
    st.success("👷 2 Inspectors Found Nearby:")
    st.markdown("""
- **SafeHome Inspections** – 4.9⭐ | $450 | Available: 2 days  
- **NSW Property Checks** – 4.7⭐ | $390 | Available: 5 days  
""")

# --- 11. Home Insurance Advisor ---
st.header("🛡️ 11. Home Insurance Match")
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
