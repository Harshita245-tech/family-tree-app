import streamlit as st
import pandas as pd
from graphviz import Digraph
import os

st.set_page_config(layout="wide")
st.title("👪 Guided Family Tree Builder")

DATA_FILE = "data.csv"

# Load or initialize data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["name", "relation_type", "related_to", "label"])

# --- ROOT NODES ---
st.header("🌳 Step 1: Add Root Ancestor Couple")

with st.form("root_form"):
    root1 = st.text_input("First Root Name (e.g., Great Grandfather)")
    root2 = st.text_input("Second Root Name (e.g., Great Grandmother)")
    root_relation = st.selectbox("Relation Between Them", ["Husband", "Wife"])
    submitted = st.form_submit_button("Add Root Couple")

if submitted:
    if root1 and root2:
        df = df._append({"name": root1, "relation_type": "Root", "related_to": "", "label": ""}, ignore_index=True)
        df = df._append({"name": root2, "relation_type": "Spouse", "related_to": root1, "label": root_relation}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Root couple added.")
        st.experimental_rerun()
    else:
        st.error("Please enter both names.")

# --- CHILDREN OF ROOT COUPLE ---
st.header("👶 Step 2: Add Children of Root Couple")

with st.form("child_form"):
    parent_name = st.selectbox("Select Parent", df['name'].tolist())
    child_names = st.text_area("Enter Children (one per line)")
    child_gender = st.selectbox("Gender of Children", ["Son", "Daughter"])
    add_children = st.form_submit_button("Add Children")

if add_children:
    if child_names and parent_name:
        for child in child_names.strip().split("\n"):
            df = df._append({"name": child.strip(), "relation_type": "Child", "related_to": parent_name, "label": child_gender}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Children added successfully.")
        st.experimental_rerun()

# --- ADD SPOUSES FOR CHILDREN ---
st.header("💍 Step 3: Add Spouses for Children")

with st.form("spouse_form"):
    person = st.selectbox("Select Family Member", df['name'].tolist())
    spouse_name = st.text_input("Enter Spouse Name")
    spouse_relation = st.selectbox("Spouse is", ["Husband", "Wife"])
    add_spouse = st.form_submit_button("Add Spouse")

if add_spouse:
    if person and spouse_name:
        df = df._append({"name": spouse_name, "relation_type": "Spouse", "related_to": person, "label": spouse_relation}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Spouse added.")
        st.experimental_rerun()

# --- GRANDCHILDREN (Children of Children) ---
st.header("🧒 Step 4: Add Grandchildren")

with st.form("grandchild_form"):
    parent = st.selectbox("Select Parent (from previous children)", df['name'].tolist())
    grandchild_names = st.text_area("Enter Grandchildren (one per line)")
    child_order = st.selectbox("Order", ["Eldest", "Middle", "Youngest"])
    add_grandchild = st.form_submit_button("Add Grandchildren")

if add_grandchild:
    if grandchild_names and parent:
        for gchild in grandchild_names.strip().split("\n"):
            df = df._append({"name": gchild.strip(), "relation_type": "Child", "related_to": parent, "label": child_order}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Grandchildren added.")
        st.experimental_rerun()

# --- OPTIONAL SPOUSES FOR GRANDCHILDREN ---
st.header("💑 Step 5: Add Spouses for Grandchildren")

with st.form("grandspouse_form"):
    grandchild = st.selectbox("Select Grandchild", df['name'].tolist())
    gspouse = st.text_input("Enter Spouse Name")
    gspouse_relation = st.selectbox("Spouse is", ["Husband", "Wife"])
    add_gspouse = st.form_submit_button("Add Spouse")

if add_gspouse:
    if grandchild and gspouse:
        df = df._append({"name": gspouse, "relation_type": "Spouse", "related_to": grandchild, "label": gspouse_relation}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Grandchild spouse added.")
        st.experimental_rerun()

# --- VISUALIZATION ---
st.subheader("📍 Family Tree Visualization")

dot = Digraph()
dot.attr(rankdir='TB')

for _, row in df.iterrows():
    person = row['name']
    related = row['related_to']
    rel_type = row['relation_type']
    label = row['label']

    dot.node(person, label=person + ("\n[" + label + "]" if label else ""))

    if rel_type == "Spouse" and related:
        dot.edge(related, person, dir="none", label="spouse", constraint='false')
    elif rel_type == "Child" and related:
        dot.edge(related, person, label="child")

st.graphviz_chart(dot)

# View/Edit Raw Data
with st.expander("🧾 View Family Data Table"):
    st.dataframe(df, use_container_width=True)

# Reset Option
with st.expander("⚠️ Reset Everything"):
    if st.button("Clear Family Tree"):
        df = pd.DataFrame(columns=["name", "relation_type", "related_to", "label"])
        df.to_csv(DATA_FILE, index=False)
        st.warning("Family tree has been cleared.")
        st.experimental_rerun()
