from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()

# Weekly data as a variable - Modified values, dynamic function name
weekly_data = """
### 7 Dec - 13 Dec    vs Baseline   vs Last week

| Function | Metric | 202550 | vs Baseline | vs Last week |
|----------|--------|--------|-------------|--------------|
| PREMIUM  | Base                           | 523.8K         | 9%          | 2%           |
|          | MAC (% of Base)                | 35%            | -285        | -127         |
|          | Weekly TPC                     | 2.15           | 712         | -389         |
|          | Weekly SPC                     | 12.3K          | -2%         | -55%         |
|          | GMV Share                      | 5.2%           | -178        | -524         |
|          | Unit share                     | 1.35%          | -15         | -19          |
|          | %Visit share                   | 0.53%          | 5           | -1           |
|          | New Activation                 | 2.1K           | 92%         | -21.45%      |
|          | Churn                          | 3.2K           | -28.73%     | -72.18%      |
|          | Mycoin balance( Liquidity ) | 102M           | 14%         | -0.98%       |
|          | Program Cost 1P                | 7.5M           | -51.23%     | -42.65%      |
"""

# Extract function name dynamically from the data
def extract_function_name(data):
    """Extract the function/program name from the data table"""
    for line in data.split('\n'):
        if '|' in line and 'Function' not in line and 'Base' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) > 1 and parts[1]:
                return parts[1]
    return "LOYALTY PROGRAM"

function_name = extract_function_name(weekly_data)

prompt = f"""Analyze {function_name} loyalty program performance and provide a concise summary of key metrics.

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
- Relationship: SPC = TPC x AOV

**GMV (Gross Merchandise Value)** [derived]
- Calculation: SPC x (Base x MAC%)
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
- Calculation: (Program GMV / Total Platform GMV) x 100
- Definition: Percentage of total platform revenue from this program
- Unit: Percentage
- Higher is better - growing market position

**Unit Share**
- Calculation: (Program Units / Total Platform Units) x 100
- Definition: Percentage of total platform units from this program
- Unit: Percentage

**% Visit Share**
- Calculation: (Program Visits / Total Platform Visits) x 100
- Definition: Percentage of total platform traffic from this program
- Unit: Percentage
- Compare with GMV share to assess conversion efficiency

### Loyalty Program Metrics:
**Mycoin Balance (Liquidity)**
- Definition: Total unredeemed Mycoin rewards held by all program customers
- Unit: Currency (M = millions, B = billions)
- Analysis: High growth may indicate low redemption (earn >> burn problem)

**Program Cost 1P**
- Definition: First-party cost to run {function_name} program (rewards, discounts, operations)
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

### Comparison Metrics:
**vs Baseline**: Change from baseline/reference period
- For percentages (MAC, shares): Expressed in basis points (bps)
  - 1 bps = 0.01 percentage points
- For absolute numbers (TPC, SPC, Activation, Churn): Expressed as percentage change
- For counts (Base): Expressed as percentage growth

**vs Last Week**: Week-over-week change from previous week
- Same interpretation rules as vs Baseline
- Critical for identifying momentum/trend changes

### Key Relationships:
- SPC = TPC x AOV
- AOV = U2O x ASP
- GMV = Base x MAC% x SPC
- Net Customer Growth = New Activation - Churn

## DATA:

{weekly_data}

## YOUR TASK:

As an e-commerce data analyst, analyze this week's performance and provide only two sections:

1. What went well - identify positive performing metrics with specific values and changes
2. What didn't go well - identify concerning metrics with specific values and changes

As an e-commerce data analyst, review this week's performance and provide a summary of what went well and what didn't go well. Identify the key metrics driving positive or negative performance, include specific numbers with baseline and week-over-week comparisons. 
Write in a professional analytical style using bullet points. Do not include any recommendations.
"""

completion = client.chat.completions.create(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=1.0,
    max_completion_tokens=8192,
    top_p=1,
    stream=True,
    stop=None
)

print("="*80)
print("BLACK PROGRAM - COMPREHENSIVE PERFORMANCE ANALYSIS")
print("Week: December 7-13, 2024")
print("="*80)
print()

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")

print("\n" + "="*80)