import streamlit as st
import pandas as pd
from graphviz import Digraph
import os

st.set_page_config(layout="wide")
st.title("🌳 Guided Family Tree Builder (With Couple Relationship)")

DATA_FILE = "data.csv"

# Load or initialize data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["name", "relation_type", "related_to", "label"])

# --- Step 1: Root Couple Entry ---
st.header("🧓 Step 1: Add Root Ancestors (Couple)")

with st.form("root_form"):
    root1 = st.text_input("Root Person 1 (e.g., Rajaram)")
    root2 = st.text_input("Root Person 2 (e.g., Radha)")
    root_relation = st.text_input("Relation between them (type 'Couple')", value="Couple")
    submitted = st.form_submit_button("Add Root Couple")

if submitted:
    if root1.strip() and root2.strip():
        df = df._append({"name": root1.strip(), "relation_type": "Root", "related_to": "", "label": ""}, ignore_index=True)
        df = df._append({"name": root2.strip(), "relation_type": "Spouse", "related_to": root1.strip(), "label": root_relation.strip()}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Root couple added.")
        st.rerun()
    else:
        st.error("Please enter both names.")

# --- Step 2: Add Children ---
st.header("👶 Step 2: Add Children of Any Member")

with st.form("child_form"):
    parent = st.selectbox("Select Parent", df['name'].unique().tolist())
    children_names = st.text_area("Enter Children (one per line)")
    child_gender = st.text_input("Gender label (e.g., Son / Daughter)")
    child_submit = st.form_submit_button("Add Children")

if child_submit:
    if children_names.strip():
        for name in children_names.strip().split("\n"):
            df = df._append({
                "name": name.strip(),
                "relation_type": "Child",
                "related_to": parent,
                "label": child_gender
            }, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Children added.")
        st.rerun()
    else:
        st.error("Please enter at least one child name.")

# --- Step 3: Add Spouse (Label: Couple) ---
st.header("💍 Step 3: Add Spouse (as Couple)")

with st.form("spouse_form"):
    person = st.selectbox("Select Person", df['name'].unique().tolist())
    spouse_name = st.text_input("Spouse Name")
    spouse_relation = st.text_input("Relation (default = Couple)", value="Couple")
    spouse_submit = st.form_submit_button("Add Spouse")

if spouse_submit:
    if person.strip() and spouse_name.strip():
        df = df._append({
            "name": spouse_name.strip(),
            "relation_type": "Spouse",
            "related_to": person,
            "label": spouse_relation.strip()
        }, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Spouse added.")
        st.rerun()
    else:
        st.error("Please enter both names.")

# --- Step 4: Add Next Generation (Grandchildren, etc.) ---
st.header("👧 Step 4: Add Children of the Next Generation")

with st.form("next_gen_form"):
    next_parent = st.selectbox("Select Parent (Any Member)", df['name'].unique().tolist())
    next_children = st.text_area("Enter Children (one per line)")
    gen_order = st.text_input("Label (e.g., Eldest / Middle / Youngest)")
    gen_submit = st.form_submit_button("Add Next Gen Children")

if gen_submit:
    if next_children.strip():
        for name in next_children.strip().split("\n"):
            df = df._append({
                "name": name.strip(),
                "relation_type": "Child",
                "related_to": next_parent,
                "label": gen_order.strip()
            }, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Next generation added.")
        st.rerun()
    else:
        st.error("Please enter names.")

# --- Family Tree Visual ---
st.subheader("📍 Family Tree Visualization")

dot = Digraph()
dot.attr(rankdir="TB")

for _, row in df.iterrows():
    name = row["name"]
    rel_type = row["relation_type"]
    related_to = row["related_to"]
    label = row["label"]

    display_label = f"{name}\n[{label}]" if label else name
    dot.node(name, label=display_label)

    if rel_type == "Spouse" and related_to:
        dot.edge(related_to, name, dir="none", label="couple", constraint="false")
    elif rel_type == "Child" and related_to:
        dot.edge(related_to, name, label="child")

st.graphviz_chart(dot)

# --- View Data ---
with st.expander("📋 Family Table"):
    st.dataframe(df)

# --- Reset All Data ---
with st.expander("⚠️ Reset Family Tree"):
    if st.button("Reset All Data"):
        df = pd.DataFrame(columns=["name", "relation_type", "related_to", "label"])
        df.to_csv(DATA_FILE, index=False)
        st.warning("Family tree reset.")
        st.rerun()
