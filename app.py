import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="QuickMed Quality Dashboard", page_icon="🏥", layout="wide")

DATA_FILE = Path(__file__).with_name("metrics.csv")

st.title("🏥 QuickMed Software Quality Dashboard")
st.caption("Continuous Software Quality and Reliability Assessment for AI-Enabled Hospital Management Systems")

if not DATA_FILE.exists():
    st.error("metrics.csv is missing. Keep it in the same folder as app.py.")
    st.stop()

df = pd.read_csv(DATA_FILE).fillna("")
required = ["Metric", "Category", "Stage", "Value", "Unit", "Threshold", "Direction", "Target", "Source", "Notes"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"metrics.csv is missing columns: {', '.join(missing)}")
    st.stop()

def numeric(v):
    try:
        if str(v).strip() == "" or str(v).strip().upper() in {"TBD", "NA", "N/A", "NOT MEASURED"}:
            return None
        return float(v)
    except (TypeError, ValueError):
        return None

def status(row):
    value = numeric(row["Value"])
    target = numeric(row["Target"])
    direction = str(row["Direction"]).strip().lower()
    if value is None or target is None or direction not in {"higher", "lower"}:
        return "Not measured"
    if direction == "higher":
        if value >= target: return "Green"
        if value >= target * 0.9: return "Amber"
        return "Red"
    else:
        if value <= target: return "Green"
        if value <= target * 1.2: return "Amber"
        return "Red"

df["Status"] = df.apply(status, axis=1)
df["Value display"] = df.apply(
    lambda r: (f'{numeric(r["Value"]):g} {r["Unit"]}'.strip() if numeric(r["Value"]) is not None else "Not measured"),
    axis=1
)

st.warning("Replace preliminary/demo values, TBD fields, and example thresholds with the team's verified measurements and agreed targets before submission.")

st.sidebar.header("Dashboard filters")
categories = ["All"] + sorted(df["Category"].astype(str).unique().tolist())
stages = ["All"] + sorted(df["Stage"].astype(str).unique().tolist())
statuses = ["All", "Green", "Amber", "Red", "Not measured"]
cat_pick = st.sidebar.selectbox("Category", categories)
stage_pick = st.sidebar.selectbox("Measurement stage", stages)
status_pick = st.sidebar.selectbox("Status", statuses)

view = df.copy()
if cat_pick != "All": view = view[view["Category"] == cat_pick]
if stage_pick != "All": view = view[view["Stage"] == stage_pick]
if status_pick != "All": view = view[view["Status"] == status_pick]

total = len(view)
measured = sum(numeric(v) is not None for v in view["Value"])
green = int((view["Status"] == "Green").sum())
attention = int(view["Status"].isin(["Amber", "Red"]).sum())
not_measured = int((view["Status"] == "Not measured").sum())

a,b,c,d = st.columns(4)
a.metric("Metrics in view", total)
b.metric("Measured", measured)
c.metric("Green", green)
d.metric("Need data / attention", attention + not_measured)

st.subheader("Metric status overview")
display_cols = ["Metric", "Category", "Stage", "Value display", "Threshold", "Status", "Source", "Notes"]
st.dataframe(view[display_cols], use_container_width=True, hide_index=True)

st.subheader("Measured metric values")
chart = view.copy()
chart["Numeric value"] = chart["Value"].apply(numeric)
chart = chart.dropna(subset=["Numeric value"])
if not chart.empty:
    chart_label = chart.apply(lambda r: f'{r["Metric"]} ({r["Stage"]})', axis=1)
    chart_data = pd.DataFrame({"Metric": chart_label, "Value": chart["Numeric value"].values}).set_index("Metric")
    st.bar_chart(chart_data, width="stretch")
    st.caption("Metric units differ, so do not compare bar heights across different units as if they were equivalent.")
else:
    st.info("No numeric measurements match the selected filters yet.")

st.subheader("Stage comparison")
comparison_metric = st.selectbox("Choose a metric to compare", sorted(df["Metric"].astype(str).unique().tolist()))
compare = df[df["Metric"] == comparison_metric].copy()
compare["Numeric value"] = compare["Value"].apply(numeric)
compare = compare.dropna(subset=["Numeric value"])
if not compare.empty:
    st.dataframe(compare[["Metric", "Stage", "Numeric value", "Unit", "Threshold", "Status", "Source"]], use_container_width=True, hide_index=True)
    st.bar_chart(compare.set_index("Stage")[["Numeric value"]], width="stretch")
else:
    st.info("This metric has no numeric values yet. Add verified values to metrics.csv to display the comparison.")

st.subheader("Usability evaluation")
st.write("Enter the actual Lighthouse scores and SUS result after completing the tests. These fields are not automatically measured by this dashboard.")
usability = df[df["Category"].astype(str).str.lower().isin(["usability", "lighthouse", "sus"])]
if not usability.empty:
    st.dataframe(usability[["Metric", "Stage", "Value display", "Threshold", "Status", "Notes"]], use_container_width=True, hide_index=True)

with st.expander("How to update metrics.csv"):
    st.markdown(
        "- Keep `metrics.csv` in the same folder as `app.py`.\n"
        "- Add one row per metric and stage (for example, Before AI, With AI, After fix).\n"
        "- `Value` must be numeric for a status to be calculated; leave it as `TBD` until measured.\n"
        "- `Target` and `Direction` must match the team's agreed threshold. `higher` means larger is better; `lower` means smaller is better.\n"
        "- `Source` should identify the test report, pipeline run, Lighthouse report, or SUS survey used."
    )

st.caption("Member 4 working dashboard • Verify all values and thresholds with the team before final submission.")
