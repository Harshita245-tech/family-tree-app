import streamlit as st
import pandas as pd
from graphviz import Digraph
import os

st.set_page_config(layout="wide")
st.title("🌳 Infinite Generation Family Tree Builder")

DATA_FILE = "data.csv"

# Load or create
df = pd.read_csv(DATA_FILE) if os.path.exists(DATA_FILE) else pd.DataFrame(columns=["name", "relation_type", "related_to", "label"])

# Sidebar Mode Selector
st.sidebar.title("⚙️ Tree Options")
mode = st.sidebar.radio("Select Mode", ["Start New Tree", "Load from Existing CSV"])
if mode == "Start New Tree":
    df = pd.DataFrame(columns=["name", "relation_type", "related_to", "label"])
    df.to_csv(DATA_FILE, index=False)
    st.info("🔄 Started a new empty tree. You can begin adding members.")
else:
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.success("📁 Loaded tree from CSV file.")
    else:
        st.warning("⚠️ No saved CSV found. Please start building the tree.")

# Step 1: Add Couple
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

# Step 2: Add Children
st.header("👶 Step 2: Add Children of a Couple")
with st.form("children_form"):
    p1 = st.selectbox("Parent 1 (e.g., Varalakshmi)", df['name'].unique().tolist(), key="p1")
    p2 = st.selectbox("Parent 2 (e.g., Rajendra Prasad)", df['name'].unique().tolist(), key="p2")
    children = st.text_area("Enter Their Children (one per line)")
    submit_children = st.form_submit_button("Add Children")
if submit_children and children:
    for name in children.strip().split("\n"):
        name = name.strip()
        df = df._append({"name": name, "relation_type": "Child", "related_to": p1, "label": "child"}, ignore_index=True)
        df = df._append({"name": name, "relation_type": "Child", "related_to": p2, "label": "child"}, ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Children added.")
    st.rerun()

# Step 3: Add Spouse of a Member
st.header("💍 Step 3: Add Spouse of a Member")
with st.form("add_spouse"):
    person = st.selectbox("Select Person", df['name'].unique().tolist(), key="s3")
    spouse = st.text_input("Spouse Name")
    add_spouse = st.form_submit_button("Add Spouse")
if add_spouse and person and spouse:
    df = df._append({"name": spouse, "relation_type": "Spouse", "related_to": person, "label": "Couple"}, ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Spouse added.")
    st.rerun()

# Step 4: Add Child with Spouse and Children
st.header("👨‍👩‍👦 Step 4: Add Child with Spouse and Their Children")
with st.form("child_spouse_form"):
    base = st.selectbox("Select a Child to Continue", df['name'].unique().tolist(), key="s4")
    base_spouse = st.text_input("Enter Spouse Name for This Child")
    grandkids = st.text_area("Enter Their Children (one per line)")
    add_branch = st.form_submit_button("Add Branch")
if add_branch and base and base_spouse and grandkids:
    df = df._append({"name": base_spouse, "relation_type": "Spouse", "related_to": base, "label": "Couple"}, ignore_index=True)
    for name in grandkids.strip().split("\n"):
        name = name.strip()
        df = df._append({"name": name, "relation_type": "Child", "related_to": base, "label": "child"}, ignore_index=True)
        df = df._append({"name": name, "relation_type": "Child", "related_to": base_spouse, "label": "child"}, ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Branch added.")
    st.rerun()

# Step 5: Add Spouse + Children for Any Child (Recursive)
st.header("🔁 Step 5: Add Spouse and Children of Any Existing Member")
with st.form("recursive_form"):
    base = st.selectbox("Select Child", df['name'].unique().tolist(), key="rc1")
    base_spouse = st.text_input("Enter Spouse Name", key="rc2")
    grandkids = st.text_area("Enter Their Children (one per line)")
    add_recursive = st.form_submit_button("Add Descendants")
if add_recursive and base and base_spouse and grandkids:
    df = df._append({"name": base_spouse, "relation_type": "Spouse", "related_to": base, "label": "Couple"}, ignore_index=True)
    for name in grandkids.strip().split("\n"):
        name = name.strip()
        df = df._append({"name": name, "relation_type": "Child", "related_to": base, "label": "child"}, ignore_index=True)
        df = df._append({"name": name, "relation_type": "Child", "related_to": base_spouse, "label": "child"}, ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Descendants added.")
    st.rerun()

# Step 6: Add Next Generation
def add_next_gen():
    st.header("📥 Step 6: Add Next Generation")
    with st.form("nextgen_form"):
        parent = st.selectbox("Select Parent", df['name'].unique().tolist(), key="ng1")
        parent_spouse = st.text_input("Enter Spouse Name", key="ng2")
        kids = st.text_area("Enter Children Names (one per line)")
        submit = st.form_submit_button("Add Next Gen")
    if submit and parent and parent_spouse and kids:
        df = df._append({"name": parent_spouse, "relation_type": "Spouse", "related_to": parent, "label": "Couple"}, ignore_index=True)
        for kid in kids.strip().split("\n"):
            df = df._append({"name": kid, "relation_type": "Child", "related_to": parent, "label": "child"}, ignore_index=True)
            df = df._append({"name": kid, "relation_type": "Child", "related_to": parent_spouse, "label": "child"}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Next generation added.")
        st.rerun()
add_next_gen()

# Step 7: Infinite Repeat
def add_more_gens():
    st.header("🔄 Step 7: Continue Adding Generations")
    with st.form("genloop_form"):
        parent = st.selectbox("Pick a Parent to Extend", df['name'].unique().tolist(), key="g7")
        spouse = st.text_input("Spouse Name")
        children = st.text_area("Children (one per line)")
        go = st.form_submit_button("Add More")
    if go and parent and spouse and children:
        df = df._append({"name": spouse, "relation_type": "Spouse", "related_to": parent, "label": "Couple"}, ignore_index=True)
        for ch in children.strip().split("\n"):
            df = df._append({"name": ch, "relation_type": "Child", "related_to": parent, "label": "child"}, ignore_index=True)
            df = df._append({"name": ch, "relation_type": "Child", "related_to": spouse, "label": "child"}, ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("New members added.")
        st.rerun()
add_more_gens()

# Step 8: Delete a Member
st.header("❌ Step 8: Delete a Member")
with st.form("delete_form"):
    to_delete = st.selectbox("Select Member to Delete", df['name'].unique().tolist())
    del_submit = st.form_submit_button("Delete Member")
if del_submit and to_delete:
    df = df[df['name'] != to_delete]
    df = df[df['related_to'] != to_delete]
    df.to_csv(DATA_FILE, index=False)
    st.warning(f"Member '{to_delete}' and related links deleted.")
    st.rerun()

# Step 9: Update Member Name
st.header("✏️ Step 9: Update Member Name")
with st.form("update_form"):
    old_name = st.selectbox("Select Member to Rename", df['name'].unique().tolist())
    new_name = st.text_input("Enter New Name")
    update_submit = st.form_submit_button("Update Name")
if update_submit and old_name and new_name:
    df['name'] = df['name'].replace(old_name, new_name)
    df['related_to'] = df['related_to'].replace(old_name, new_name)
    df.to_csv(DATA_FILE, index=False)
    st.success(f"Updated name from '{old_name}' to '{new_name}'")
    st.rerun()

# Tree Rendering
st.subheader("📍 Visual Family Tree")
dot = Digraph()
dot.attr(rankdir="TB")
couples = set()

for _, row in df.iterrows():
    name, related_to, rel_type, label = row["name"], row["related_to"], row["relation_type"], row["label"]
    dot.node(name)
    if rel_type == "Spouse" and related_to:
        couple_id = f"{min(name, related_to)}_{max(name, related_to)}"
        if couple_id not in couples:
            dot.node(couple_id, shape="point", width="0")
            dot.edge(related_to, couple_id, dir="none", label="couple")
            dot.edge(name, couple_id, dir="none")
            couples.add(couple_id)
    elif rel_type == "Child" and related_to:
        for _, partner_row in df[(df['name'] == related_to) & (df['relation_type'] == 'Spouse')].iterrows():
            partner = partner_row['related_to']
            couple_id = f"{min(related_to, partner)}_{max(related_to, partner)}"
            if couple_id in couples:
                dot.edge(couple_id, name, label="child")
                break
        else:
            dot.edge(related_to, name, label="child")

st.graphviz_chart(dot)

with st.expander("📋 View Table"):
    st.dataframe(df)

with st.expander("⚠️ Reset Tree"):
    if st.button("Clear All Data"):
        df = pd.DataFrame(columns=["name", "relation_type", "related_to", "label"])
        df.to_csv(DATA_FILE, index=False)
        st.warning("All data cleared.")
        st.rerun()
