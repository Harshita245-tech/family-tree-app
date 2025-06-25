import streamlit as st
import pandas as pd
from graphviz import Digraph
import os

st.set_page_config(layout="wide")
st.title("🌳 Infinite Generation Family Tree Builder")

DATA_FILE = "data.csv"

# Load or create
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["name", "relation_type", "related_to", "label"])

# --- Step 1: Add Couple ---
st.header("👩‍❤️‍👨 Step 1: Add Couple")
with st.form("couple_form"):
    person1 = st.text_input("First Person Name")
    person2 = st.text_input("Second Person Name")
    add_couple = st.form_submit_button("Add Couple")

if add_couple:
    if person1 and person2:
        df = df._append({"name": person1, "relation_type": "Root", "related_to": "", "label": ""}, ignore_index=True)
        df = df._append({"name": person2, "relation_type": "Spouse", "related_to": person1, "label": "Couple"}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Couple added.")
        st.rerun()
    else:
        st.error("Please enter both names.")

# --- Step 2: Add Children from Couple ---
st.header("🧒 Step 2: Add Children from a Couple")
with st.form("child_form"):
    parent1 = st.selectbox("Select First Parent", df['name'].unique().tolist(), key="p1")
    parent2 = st.selectbox("Select Second Parent", df['name'].unique().tolist(), key="p2")
    children_names = st.text_area("Enter Child Names (one per line)")
    add_child = st.form_submit_button("Add Children")

if add_child:
    if parent1 and parent2 and children_names:
        for child_name in children_names.strip().split("\n"):
            df = df._append({"name": child_name.strip(), "relation_type": "Child", "related_to": parent1, "label": "child"}, ignore_index=True)
            df = df._append({"name": child_name.strip(), "relation_type": "Child", "related_to": parent2, "label": "child"}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Children added from couple.")
        st.rerun()
    else:
        st.error("Please enter both parents and at least one child.")

# --- Step 3: Add Children of Varalakshmi and Rajendra Prasad ---
st.header("👧 Step 3: Add Children of a Specific Couple")
with st.form("child_specific_form"):
    couple_parent1 = st.selectbox("Parent 1 (e.g., Varalakshmi)", df['name'].unique().tolist(), key="cp1")
    couple_parent2 = st.selectbox("Parent 2 (e.g., Rajendra Prasad)", df['name'].unique().tolist(), key="cp2")
    couple_children = st.text_area("Enter Their Children (one per line)")
    couple_submit = st.form_submit_button("Add Children")

if couple_submit:
    if couple_parent1 and couple_parent2 and couple_children:
        for name in couple_children.strip().split("\n"):
            df = df._append({"name": name.strip(), "relation_type": "Child", "related_to": couple_parent1, "label": "child"}, ignore_index=True)
            df = df._append({"name": name.strip(), "relation_type": "Child", "related_to": couple_parent2, "label": "child"}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Children added.")
        st.rerun()
    else:
        st.error("Please enter both parents and children.")

# --- Step 4: Add Next Gen Descendants for Children (Manual Infinite Flow) ---
st.header("🔁 Step 4: Add Child with Spouse and Their Children")
with st.form("multi_gen_form"):
    child = st.selectbox("Select a Child to Continue", df['name'].unique().tolist(), key="cg1")
    child_spouse = st.text_input("Enter Spouse Name for This Child")
    child_children = st.text_area("Enter Their Children (one per line)")
    multi_submit = st.form_submit_button("Add Spouse + Children")

if multi_submit:
    if child and child_spouse:
        df = df._append({"name": child_spouse.strip(), "relation_type": "Spouse", "related_to": child, "label": "Couple"}, ignore_index=True)
        if child_children.strip():
            for name in child_children.strip().split("\n"):
                df = df._append({"name": name.strip(), "relation_type": "Child", "related_to": child, "label": "child"}, ignore_index=True)
                df = df._append({"name": name.strip(), "relation_type": "Child", "related_to": child_spouse.strip(), "label": "child"}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("New generation added.")
        st.rerun()
    else:
        st.error("Please provide both child and their spouse.")

# --- Render Family Tree ---
st.subheader("📍 Visual Family Tree")
dot = Digraph()
dot.attr(rankdir="TB")

for _, row in df.iterrows():
    name = row["name"]
    related_to = row["related_to"]
    rel_type = row["relation_type"]
    label = row["label"]

    dot.node(name)
    if rel_type == "Spouse" and related_to:
        dot.edge(related_to, name, dir="none", label="couple", constraint="false")
    elif rel_type == "Child" and related_to:
        dot.edge(related_to, name, label="child")

st.graphviz_chart(dot)

# --- View / Reset ---
with st.expander("📋 View Table"):
    st.dataframe(df)

with st.expander("⚠️ Reset Tree"):
    if st.button("Clear All Data"):
        df = pd.DataFrame(columns=["name", "relation_type", "related_to", "label"])
        df.to_csv(DATA_FILE, index=False)
        st.warning("All data cleared.")
        st.rerun()
