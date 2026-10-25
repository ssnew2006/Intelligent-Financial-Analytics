# 📊 Intelligent Financial Analytics (Diminishing Musharakah)

An end-to-end Data Science and Full-Stack web application designed to parse, analyze, and visualize Shariah-compliant Islamic financing contracts (*Diminishing Musharakah*). This project bridges the gap between unstructured legal documentation and automated financial engineering.

---

## Key Features

* **Intelligent Document Processing (IDP):** Automatically ingests raw multi-page legal PDF contracts, scans text using Regex patterns, and extracts core financial variables (Property Value, Investor Capital, Tenure) on the fly.
* **6-Tab Interactive Dashboard:** Built with **Streamlit** to provide an intuitive, responsive user experience:
  1. **Overview:** High-level summary metrics, capital structure donut charts, and complete 120-month payment grids.
  2. **Performance Metrics:** Interactive yearly heatmap visualizing payment intensity and cash-flow distribution across the 10-year lifecycle with embedded exact values.
  3. **Property List:** Master registry tracking active real estate assets, locations, and investor shares.
  4. **Analytics:** Advanced 10-year amortization curves tracking absolute capital balance reduction in real-time.
  5. **Risk Allocation:** Evaluates relative risk exposure reduction trajectories (%) and computes statistical payment volatility (Standard Deviation).
  6. **Compliance:** Shariah governance audits verifying AAOIFI standards (*Shirkat-ul-Milk, Ijarah, Wa'ad*).
* **Automated Mathematical Modeling:** Leverages **Pandas** and **NumPy** to calculate declining rental shares and monthly unit buyouts dynamically.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Frontend & UI:** Streamlit
* **Data Processing & Analysis:** Pandas, NumPy
* **Data Visualization:** Plotly Express & Graph Objects
* **Document Parsing:** PyPDF2, Regular Expressions (Re)

---

## ⚙️ Installation & Setup Guide

Follow these steps to set up and run the application locally in Visual Studio Code:

### 1. Clone or Open Project Directory
Navigate to your project folder in your terminal:
```bash
cd path/to/your/project

# 2. Create & Activate a Virtual Environment
Bash
# Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 4. Install Dependencies
Install the required data science and web framework libraries:

Bash
pip install --default-timeout=100 --retries 10 streamlit pandas numpy plotly PyPDF2


# 5. Run the Streamlit Application
Launch the dashboard locally:

Bash
streamlit run app.py

---

📈 Financial Methodology (Diminishing Musharakah)The application models a co-ownership structure where the financier (Investor) and client (Buyer) jointly own a property. Over a 10-year (120-month) tenor:

- Rental Share: Calculated dynamically based on the financier's remaining principal balance:


$$\text{Rental Share} = \frac{\text{Current Balance} \times \text{Annual Rate}}{12}$$

- Unit Buyout (Redemption): Fixed monthly principal repayment:


$$\text{Unit Redemption} = \frac{\text{Initial Investor Capital}}{\text{Total Months (120)}}$$

---

💼 Portfolio Highlights for Engineering & Data RolesDemonstrates proficiency in unstructured data extraction (IDP).Showcases full-stack productization of machine learning/analytics models using Streamlit.Applies rigorous statistical modeling (Volatility, Exposure Analysis, Matrix Pivoting) to financial instruments.