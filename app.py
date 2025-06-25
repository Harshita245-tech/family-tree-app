import streamlit as st
import pandas as pd
from graphviz import Digraph
import os

st.set_page_config(layout="wide")
st.title("👨‍👩‍👧 Family Tree - Custom Diagram Style (as per sketch)")

DATA_FILE = "data.csv"

# Load or initialize
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["name", "relation_type", "related_to", "label"])

# Form to add family member
st.header("➕ Add Family Member (Same Structure as Your Diagram)")

with st.form("add_form"):
    name = st.text_input("Name (e.g., Rajendra Prasad)")
    relation_type = st.selectbox("Relation Type", ["Root", "Spouse", "Child"])
    related_to = st.text_input("Related To (Existing Person’s Name)")
    label = st.text_input("Label (e.g., Daughter, Husband, CW, etc.)")
    submitted = st.form_submit_button("Add to Tree")

if submitted:
    if not name.strip():
        st.error("Name is required.")
    else:
        df = df._append({
            "name": name.strip(),
            "relation_type": relation_type,
            "related_to": related_to.strip(),
            "label": label.strip()
        }, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"{name.strip()} added!")
        st.experimental_rerun()

# Display tree
st.subheader("📍 Generated Tree (Like Sketch)")
dot = Digraph(format="png")
dot.attr(rankdir='TB')  # Top to bottom

for _, row in df.iterrows():
    name = row["name"]
    related = row["related_to"]
    rel_type = row["relation_type"]
    label = row["label"]

    dot.node(name, label=name + ("\n[" + label + "]" if label else ""))

    if rel_type == "Spouse" and related:
        dot.edge(related, name, dir="none", label="spouse", constraint='false')
    elif rel_type == "Child" and related:
        dot.edge(related, name, label="child")
    elif rel_type == "Root":
        dot.node(name)

st.graphviz_chart(dot)

# Table viewer
with st.expander("🧾 Family Data Table"):
    st.dataframe(df, use_container_width=True)

# Reset option
with st.expander("⚠️ Reset Tree"):
    if st.button("Delete All Data"):
        df = pd.DataFrame(columns=["name", "relation_type", "related_to", "label"])
        df.to_csv(DATA_FILE, index=False)
        st.warning("All family data cleared.")
        st.experimental_rerun()
