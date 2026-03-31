import streamlit as st
import pandas as pd

# ================= PAGE CONFIG =================
st.set_page_config(page_title="UBI Dashboard", layout="wide")

# ================= CUSTOM CSS =================
st.markdown("""
<style>

body {
    background-color: #f5f1e6;
}

.main {
    background-color: #f5f1e6;
}

h1, h2, h3, h4 {
    color: #333333;
    font-weight: 700;
}

.big-font {
    font-size:22px !important;
}

.kpi-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}

.kpi-title {
    font-size:18px;
    color: #666;
}

.kpi-value {
    font-size:32px;
    font-weight:bold;
    color:#2c3e50;
}

.search-box input {
    font-size:18px !important;
    padding:10px !important;
}

</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
file_path = r"D:\WORK\UBI Employee Data\EAP for UBI by HFN\UBI Dashboard - Dashboard.csv"
df = pd.read_csv(file_path)

# ================= TITLE =================
st.markdown("<h1 style='font-size:40px;'>📊 UBI Employee Dashboard</h1>", unsafe_allow_html=True)

# ================= SEARCH =================
search = st.text_input("🔍 Search by Employee ID / Phone / Name")

# ================= SEARCH RESULT =================
if search:

    result = df[
        (df["EMPLID"].astype(str) == search) |
        (df["PHONE"].astype(str) == search) |
        (df["NAME"].str.lower() == search.lower())
    ]

    if not result.empty:
        st.success("Employee Found ✅")

        for _, row in result.iterrows():
            st.markdown(f"""
            <div class="kpi-card">
                <h2>{row['NAME']}</h2>
                <p class="big-font"><b>EMPLID:</b> {row['EMPLID']}</p>
                <p class="big-font"><b>PHONE:</b> {row['PHONE']}</p>
                <p class="big-font"><b>EMAIL:</b> {row['EMAIL']}</p>
                <p class="big-font"><b>Group:</b> {row['Group']}</p>
                <p class="big-font"><b>Zone:</b> {row['Zone']}</p>
                <p class="big-font"><b>Status:</b> {row['STATUS']}</p>
                <p class="big-font"><b>Issue:</b> {row['ISSUE']}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("No Employee Found ❌")

# ================= DASHBOARD =================
else:

    st.markdown("<h2 style='font-size:30px;'>📌 Key Metrics</h2>", unsafe_allow_html=True)

    total = len(df)
    onboarded = len(df[df["STATUS"] == "Onboarded"])
    mismatch = len(df[df["ISSUE"] == "Data Mismatch"])
    unverified = len(df[df["ISSUE"] == "Unverified"])

    col1, col2, col3, col4 = st.columns(4)

    def kpi(title, value):
        return f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """

    col1.markdown(kpi("Total Participants", total), unsafe_allow_html=True)
    col2.markdown(kpi("Total Onboarded", onboarded), unsafe_allow_html=True)
    col3.markdown(kpi("Data Mismatch", mismatch), unsafe_allow_html=True)
    col4.markdown(kpi("Unverified", unverified), unsafe_allow_html=True)

    # ================= CHARTS =================
    st.markdown("<h2 style='font-size:30px;'>📊 Insights</h2>", unsafe_allow_html=True)

    col5, col6 = st.columns(2)

    with col5:
        st.markdown("<p class='big-font'><b>Zone-wise Distribution</b></p>", unsafe_allow_html=True)
        st.line_chart(df["Zone"].value_counts())

    with col6:
        st.markdown("<p class='big-font'><b>Issue Distribution</b></p>", unsafe_allow_html=True)
        st.bar_chart(df["ISSUE"].value_counts())

    # ================= TABLES =================
    st.markdown("<h2 style='font-size:30px;'>📋 Group-wise Count</h2>", unsafe_allow_html=True)
    group_table = df.groupby("Group").size().reset_index(name="Count")
    st.dataframe(group_table)

    st.markdown("<h2 style='font-size:30px;'>📋 Status Summary</h2>", unsafe_allow_html=True)
    status_table = df.groupby("STATUS").size().reset_index(name="Count")
    st.dataframe(status_table)