import streamlit as st
import pandas as pd
from graphviz import Digraph
import os

st.set_page_config(layout="wide")
st.title("🌳 Infinite Generation Family Tree Builder")

DATA_FILE = "data.csv"

# Load or create
df = pd.read_csv(DATA_FILE) if os.path.exists(DATA_FILE) else pd.DataFrame(columns=["name", "relation_type", "related_to", "label"])

# --- Step 1: Add Couple ---
st.header("👩‍❤️‍👨 Step 1: Add Couple")
with st.form("couple_form"):
    person1 = st.text_input("First Person Name")
    person2 = st.text_input("Second Person Name")
    add_couple = st.form_submit_button("Add Couple")
if add_couple and person1 and person2:
    df = df._append({"name": person1, "relation_type": "Root", "related_to": "", "label": ""}, ignore_index=True)
    df = df._append({"name": person2, "relation_type": "Spouse", "related_to": person1, "label": "Couple"}, ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Couple added.")
    st.rerun()

# --- Step 2: Add Children from Couple ---
st.header("🧒 Step 2: Add Children from a Couple")
with st.form("child_form"):
    parent1 = st.selectbox("Select First Parent", df['name'].unique().tolist(), key="p1")
    parent2 = st.selectbox("Select Second Parent", df['name'].unique().tolist(), key="p2")
    children_names = st.text_area("Enter Child Names (one per line)")
    add_child = st.form_submit_button("Add Children")
if add_child and parent1 and parent2 and children_names:
    for child_name in children_names.strip().split("\n"):
        df = df._append({"name": child_name.strip(), "relation_type": "Child", "related_to": parent1, "label": "child"}, ignore_index=True)
        df = df._append({"name": child_name.strip(), "relation_type": "Child", "related_to": parent2, "label": "child"}, ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Children added from couple.")
    st.rerun()

# --- Step 3: Add Spouse to a Member ---
st.header("💍 Step 3: Add Spouse of a Member")
with st.form("spouse_form"):
    member = st.selectbox("Select Person", df['name'].unique().tolist(), key="s1")
    spouse = st.text_input("Spouse Name")
    spouse_submit = st.form_submit_button("Add Spouse")
if spouse_submit and member and spouse:
    df = df._append({"name": spouse.strip(), "relation_type": "Spouse", "related_to": member, "label": "Couple"}, ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Spouse added.")
    st.rerun()

# --- Step 4: Add Children of This Couple ---
st.header("👶 Step 4: Add Children of a Specific Couple")
with st.form("add_children_form"):
    p1 = st.selectbox("Parent 1", df['name'].unique().tolist(), key="c1")
    p2 = st.selectbox("Parent 2", df['name'].unique().tolist(), key="c2")
    new_kids = st.text_area("Enter Their Children (one per line)")
    kid_submit = st.form_submit_button("Add Children")
if kid_submit and p1 and p2 and new_kids:
    for kid in new_kids.strip().split("\n"):
        df = df._append({"name": kid.strip(), "relation_type": "Child", "related_to": p1, "label": "child"}, ignore_index=True)
        df = df._append({"name": kid.strip(), "relation_type": "Child", "related_to": p2, "label": "child"}, ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Children added.")
    st.rerun()

# --- Step 5: Add Child's Spouse and Their Children ---
st.header("🔁 Step 5: Add Spouse and Children of Any Child")
with st.form("recursive_form"):
    base = st.selectbox("Select Child", df['name'].unique().tolist(), key="rc1")
    base_spouse = st.text_input("Enter Spouse Name for This Child")
    grandkids = st.text_area("Enter Their Children (one per line)")
    add_recursive = st.form_submit_button("Add Descendants")
if add_recursive and base and base_spouse:
    df = df._append({"name": base_spouse.strip(), "relation_type": "Spouse", "related_to": base, "label": "Couple"}, ignore_index=True)
    for name in grandkids.strip().split("\n"):
        df = df._append({"name": name.strip(), "relation_type": "Child", "related_to": base, "label": "child"}, ignore_index=True)
        df = df._append({"name": name.strip(), "relation_type": "Child", "related_to": base_spouse.strip(), "label": "child"}, ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Descendants added.")
    st.rerun()

# --- Step 6: Add More Generations (Recursive Loop) ---
st.header("♾️ Step 6: Add Next Generation from Any Child")
with st.form("gen6"):
    child = st.selectbox("Select a Child to Continue", df['name'].unique().tolist(), key="g61")
    child_spouse = st.text_input("Enter Spouse Name for This Child")
    child_children = st.text_area("Enter Their Children (one per line)")
    gen_submit = st.form_submit_button("Add Next Gen")
if gen_submit and child and child_spouse:
    df = df._append({"name": child_spouse.strip(), "relation_type": "Spouse", "related_to": child, "label": "Couple"}, ignore_index=True)
    for name in child_children.strip().split("\n"):
        df = df._append({"name": name.strip(), "relation_type": "Child", "related_to": child, "label": "child"}, ignore_index=True)
        df = df._append({"name": name.strip(), "relation_type": "Child", "related_to": child_spouse.strip(), "label": "child"}, ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Generation added.")
    st.rerun()

# --- Step 7: Add Next Generation Again ---
st.header("🧬 Step 7: Continue Generations Forever")
with st.form("gen7"):
    base = st.selectbox("Select Child from Any Gen", df['name'].unique().tolist(), key="g71")
    partner = st.text_input("Enter Their Spouse")
    next_kids = st.text_area("Enter Their Children (one per line)")
    gen7_submit = st.form_submit_button("Continue Line")
if gen7_submit and base and partner:
    df = df._append({"name": partner.strip(), "relation_type": "Spouse", "related_to": base, "label": "Couple"}, ignore_index=True)
    for name in next_kids.strip().split("\n"):
        df = df._append({"name": name.strip(), "relation_type": "Child", "related_to": base, "label": "child"}, ignore_index=True)
        df = df._append({"name": name.strip(), "relation_type": "Child", "related_to": partner.strip(), "label": "child"}, ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("New generation continued.")
    st.rerun()

# --- Render Tree ---
st.subheader("📍 Visual Family Tree")
dot = Digraph()
dot.attr(rankdir="TB")
for _, row in df.iterrows():
    name, related_to, rel_type, label = row["name"], row["related_to"], row["relation_type"], row["label"]
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
