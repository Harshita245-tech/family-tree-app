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

# --- Step 3: Add Spouse ---
st.header("💍 Step 3: Add Spouse of a Member")
with st.form("spouse_form"):
    person = st.selectbox("Select Person", df['name'].unique().tolist(), key="sp1")
    spouse_name = st.text_input("Spouse Name")
    spouse_submit = st.form_submit_button("Add Spouse")

if spouse_submit:
    if person and spouse_name:
        df = df._append({"name": spouse_name.strip(), "relation_type": "Spouse", "related_to": person, "label": "Couple"}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Spouse added.")
        st.rerun()
    else:
        st.error("Enter both names.")

# --- Step 4: Add Next Gen Children (Repeatable for Infinite Generations) ---
st.header("👶 Step 4: Add Next Generation Children (Repeatable)")
with st.form("next_gen_form"):
    parent1 = st.selectbox("Parent 1", df['name'].unique().tolist(), key="np1")
    parent2 = st.selectbox("Parent 2", df['name'].unique().tolist(), key="np2")
    next_gen_names = st.text_area("Enter Children (one per line)")
    next_gen_submit = st.form_submit_button("Add Children")

if next_gen_submit:
    if parent1 and parent2 and next_gen_names:
        for name in next_gen_names.strip().split("\n"):
            df = df._append({"name": name.strip(), "relation_type": "Child", "related_to": parent1, "label": "child"}, ignore_index=True)
            df = df._append({"name": name.strip(), "relation_type": "Child", "related_to": parent2, "label": "child"}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Children added.")
        st.rerun()
    else:
        st.error("Please enter all required fields.")

# --- Step 5: Continue Descendants (Repeatable for Infinite Generations) ---
st.header("🔁 Step 5: Add Spouse and Children of Any Existing Member")
with st.form("descendants_form"):
    parent = st.selectbox("Select Parent (who has a spouse already added)", df['name'].unique().tolist(), key="dp1")
    spouse = st.selectbox("Select Spouse of Parent", df['name'].unique().tolist(), key="dp2")
    children = st.text_area("Enter Their Children (one per line)")
    desc_submit = st.form_submit_button("Add Descendants")

if desc_submit:
    if parent and spouse and children:
        for name in children.strip().split("\n"):
            df = df._append({"name": name.strip(), "relation_type": "Child", "related_to": parent, "label": "child"}, ignore_index=True)
            df = df._append({"name": name.strip(), "relation_type": "Child", "related_to": spouse, "label": "child"}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Descendant children added.")
        st.rerun()
    else:
        st.error("Please select both parents and at least one child.")

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
