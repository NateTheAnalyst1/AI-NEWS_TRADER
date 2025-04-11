import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

TRADE_LOG = "trades.csv"

def load_trades():
    if os.path.exists(TRADE_LOG):
        return pd.read_csv(TRADE_LOG)
    else:
        return pd.DataFrame(columns=["Date", "Title", "Action", "Summary", "Status", "Result"])

def save_trade(trade):
    df = load_trades()
    df = pd.concat([df, pd.DataFrame([trade])], ignore_index=True)
    df.to_csv(TRADE_LOG, index=False)

def update_trade_status(index, new_status, result=None):
    df = load_trades()
    df.at[index, "Status"] = new_status
    if result:
        df.at[index, "Result"] = result
    df.to_csv(TRADE_LOG, index=False)

# UI Setup
st.set_page_config(page_title="Trade Tracker", layout="wide")
st.title("📈 Trade Positions Tracker")

# New Trade Entry
with st.expander("➕ Add New Trade"):
    title = st.text_input("Title")
    action = st.selectbox("Action", ["Buy", "Sell"])
    summary = st.text_area("Summary")
    if st.button("Add Trade"):
        if title and summary:
            trade = {
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Title": title,
                "Action": action,
                "Summary": summary,
                "Status": "Open",
                "Result": ""
            }
            save_trade(trade)
            st.success("Trade added successfully!")

# Load and display trades
df = load_trades()

if not df.empty:
    st.subheader("📊 Trade Overview")

    # Pie chart: Buy vs Sell
    st.markdown("**Buy vs Sell**")
    action_counts = df['Action'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(action_counts, labels=action_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    # Bar chart: Open vs Closed
    st.markdown("**Open vs Closed**")
    status_counts = df['Status'].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.bar(status_counts.index, status_counts.values, color=['green', 'red'])
    st.pyplot(fig2)

    # Line chart: Trades Over Time
    st.markdown("**Trades Over Time**")
    df['Date'] = pd.to_datetime(df['Date'])
    df_grouped = df.groupby(df['Date'].dt.date).size()
    fig3, ax3 = plt.subplots()
    ax3.plot(df_grouped.index, df_grouped.values, marker='o', linestyle='-')
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Number of Trades")
    ax3.set_title("Trade Frequency")
    st.pyplot(fig3)

    # Trade Table
    st.subheader("📋 Trade Log")
    st.dataframe(df)

    # Trade Close and Result Input
    index_to_update = st.number_input("Index to mark Closed", min_value=0, max_value=len(df)-1, step=1)
    result = st.selectbox("Result", ["Successful", "Unsuccessful"])
    if st.button("Mark as Closed"):
        update_trade_status(index_to_update, "Closed", result)
        st.success("Trade marked as Closed")

    # Success Rate
    st.subheader("✅ Trade Success Rate")
    if "Result" in df.columns and not df["Result"].isnull().all():
        closed_trades = df[df["Status"] == "Closed"]
        if not closed_trades.empty:
            success_count = (closed_trades["Result"] == "Successful").sum()
            success_rate = (success_count / len(closed_trades)) * 100
            st.metric(label="Success Rate", value=f"{success_rate:.1f}%")
        else:
            st.info("No closed trades to calculate success rate.")
    else:
        st.info("No results recorded yet.")
else:
    st.info("No trades logged yet.")

