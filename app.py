import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="BLACK Program Analyzer",
    page_icon="📊",
    layout="wide"
)

# Initialize Groq client
@st.cache_resource
def get_groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

client = get_groq_client()

# Title
st.title("📊 BLACK Loyalty Program Analyzer")
st.markdown("---")

# Weekly data input
st.subheader("Weekly Performance Data")
weekly_data = st.text_area(
    "Paste your weekly data here:",
    value="""### 7 Dec - 13 Dec    vs Baseline   vs Last week

| Function | Metric | 202550 | vs Baseline | vs Last week |
|----------|--------|--------|-------------|--------------|
| BLACK    | Base                           | 507.5K         | 7%          | 0%           |
|          | MAC (% of Base)                | 32%            | -361        | -153         |
|          | Weekly TPC                     | 1.99           | 679         | -432         |
|          | Weekly SPC                     | 11.5K          | -4%         | -60%         |
|          | GMV Share                      | 4.9%           | -203        | -589         |
|          | Unit share                     | 1.20%          | -18         | -22          |
|          | %Visit share                   | 0.49%          | 2           | -2           |
|          | New Activation                 | 1.7K           | 85%         | -26.26%      |
|          | Churn                          | 3.7K           | -24.54%     | -78.46%      |
|          | Supercoin balance( Liquidity ) | 96M            | 11%         | -1.55%       |
|          | Program Cost 1P                | 8.1M           | -46.99%     | -38.17%      |""",
    height=300
)

# Analyze button
if st.button("🔍 Analyze Performance", type="primary", use_container_width=True):
    if not weekly_data:
        st.warning("⚠️ Please provide weekly data.")
    else:
        with st.spinner("🤖 Analyzing data..."):
            # Prepare the prompt
            prompt = f"""Analyze BLACK loyalty program performance and provide a concise summary of key metrics.

## METRIC DEFINITIONS:

### Customer Base Metrics:
**Base**: Total registered customers in the program
- Unit: Count (K = thousands, M = millions)

**MAC (Monthly Active Customers as % of Base)**
- Calculation: (Monthly Active Customers / Base) × 100
- Definition: Percentage of enrolled customers who transacted in the month
- Unit: Percentage
- Higher is better - indicates engagement level

### Transaction Metrics:
**Weekly TPC (Transactions Per Customer)**
- Calculation: Total Orders / Total Active Customers
- Definition: Average number of orders per active customer during the week
- Unit: Ratio
- Higher is better - indicates purchase frequency and engagement

**U2O (Units to Orders Ratio)** [derived]
- Calculation: Total Units Sold / Total Orders
- Definition: Average items purchased per order (basket size)
- Unit: Ratio
- Higher is better - larger basket sizes

### Revenue Metrics:
**Weekly SPC (Sales Per Customer)**
- Calculation: Total GMV / Total Active Customers
- Definition: Average revenue generated per active customer during the week
- Unit: Currency (K = thousands)
- Higher is better - indicates customer value
- Relationship: SPC = TPC × AOV

**GMV (Gross Merchandise Value)** [derived]
- Calculation: SPC × (Base × MAC%)
- Definition: Total value of all goods sold
- Unit: Currency

**AOV (Average Order Value)** [derived]
- Calculation: SPC / TPC or GMV / Total Orders
- Definition: Average revenue per transaction
- Unit: Currency
- Relationship: AOV = SPC / TPC

**ASP (Average Selling Price)** [derived]
- Calculation: GMV / Total Units or AOV / U2O
- Definition: Average price per unit sold
- Unit: Currency

### Market Share Metrics:
**GMV Share**
- Calculation: (Program GMV / Total Platform GMV) × 100
- Definition: Percentage of total platform revenue from this program
- Unit: Percentage
- Higher is better - growing market position

**Unit Share**
- Calculation: (Program Units / Total Platform Units) × 100
- Definition: Percentage of total platform units from this program
- Unit: Percentage

**% Visit Share**
- Calculation: (Program Visits / Total Platform Visits) × 100
- Definition: Percentage of total platform traffic from this program
- Unit: Percentage
- Compare with GMV share to assess conversion efficiency

### Loyalty Program Metrics:
**Supercoin Balance (Liquidity)**
- Definition: Total unredeemed supercoin rewards held by all program customers
- Unit: Currency (M = millions, B = billions)
- Analysis: High growth may indicate low redemption (earn >> burn problem)

**Program Cost 1P**
- Definition: First-party cost to run BLACK program (rewards, discounts, operations)
- Unit: Currency (M = millions)
- Lower is better IF performance maintained - indicates efficiency

### Customer Lifecycle Metrics:
**New Activation**
- Definition: New customers who enrolled AND made first transaction this week
- Unit: Count (K = thousands)
- Higher is better - indicates customer acquisition success

**Churn**
- Definition: Previously active customers who became inactive or left the program
- Unit: Count (K = thousands)
- Lower is better - high churn indicates retention problems
- Critical: Compare Activation vs Churn for net customer growth

### Key Relationships:
- SPC = TPC × AOV
- AOV = U2O × ASP
- GMV = Base × MAC% × SPC
- Net Customer Growth = New Activation - Churn

## DATA:

{weekly_data}

## YOUR TASK:

As an e-commerce data analyst, analyze this week's performance and provide a professional performance summary with two sections:

**Positive Performance Indicators**
**Areas of Concern**

Identify key metrics driving performance in each section. Include specific values with baseline and week-over-week comparisons. Write in a professional analytical style using bullet points. Do not include recommendations or implications.
"""
            try:
                # Stream the response
                completion = client.chat.completions.create(
                    model="meta-llama/llama-4-maverick-17b-128e-instruct",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_completion_tokens=2048,
                    top_p=1,
                    stream=True,
                    stop=None
                )
                
                # Display streaming response
                st.subheader("📈 Analysis Result")
                response_placeholder = st.empty()
                full_response = ""
                
                for chunk in completion:
                    content = chunk.choices[0].delta.content or ""
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Make sure your GROQ_API_KEY is set in the .env file or as an environment variable.")