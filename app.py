import streamlit as st
import pandas as pd
from graphviz import Digraph
import os

st.set_page_config(layout="wide")
st.title("🌳 Infinite Generation Family Tree Builder")

DATA_FILE = "data.csv"

# Load or create DataFrame
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
    p1 = st.selectbox("Parent 1", df['name'].unique().tolist(), key="p1")
    p2 = st.selectbox("Parent 2", df['name'].unique().tolist(), key="p2")
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

# Step 7: Infinite Repeat
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

# Step 8: Delete a Member
st.header("🗑️ Step 8: Delete a Member")
with st.form("delete_member"):
    to_delete = st.selectbox("Select Member to Delete", df['name'].unique().tolist(), key="del1")
    delete_btn = st.form_submit_button("Delete")
if delete_btn:
    df = df[df['name'] != to_delete]
    df = df[df['related_to'] != to_delete]
    df.to_csv(DATA_FILE, index=False)
    st.success(f"Deleted {to_delete} and related links.")
    st.rerun()

# Step 9: Rename a Member
st.header("✏️ Step 9: Rename a Member")
with st.form("rename_member"):
    old_name = st.selectbox("Select Member to Rename", df['name'].unique().tolist(), key="up1")
    new_name = st.text_input("Enter New Name", key="up2")
    update_btn = st.form_submit_button("Update Name")
if update_btn and new_name:
    df['name'] = df['name'].replace(old_name, new_name)
    df['related_to'] = df['related_to'].replace(old_name, new_name)
    df.to_csv(DATA_FILE, index=False)
    st.success(f"Renamed {old_name} to {new_name}.")
    st.rerun()

# Render Tree
st.subheader("📍 Visual Family Tree")
dot = Digraph()
dot.attr(rankdir="TB")
couple_nodes = {}
added_edges = set()

for name in df['name'].unique():
    dot.node(name)

for _, row in df.iterrows():
    name = row['name']
    related_to = row['related_to']
    relation_type = row['relation_type']
    if relation_type == 'Spouse' and related_to:
        couple_id = tuple(sorted([name, related_to]))
        if couple_id not in couple_nodes:
            node_id = f"{couple_id[0]}_{couple_id[1]}_node"
            couple_nodes[couple_id] = node_id
            dot.node(node_id, shape="point", width="0", label="")
            dot.edge(couple_id[0], node_id, dir="none", label="couple")
            dot.edge(couple_id[1], node_id, dir="none")

for _, row in df.iterrows():
    name = row['name']
    related_to = row['related_to']
    relation_type = row['relation_type']
    if relation_type == 'Child' and related_to:
        for couple, couple_node in couple_nodes.items():
            if related_to in couple:
                if (couple_node, name) not in added_edges:
                    dot.edge(couple_node, name, label="child")
                    added_edges.add((couple_node, name))
                break

st.graphviz_chart(dot)

with st.expander("📋 View Table"):
    st.dataframe(df)

with st.expander("⚠️ Reset Tree"):
    if st.button("Clear All Data"):
        df = pd.DataFrame(columns=["name", "relation_type", "related_to", "label"])
        df.to_csv(DATA_FILE, index=False)
        st.warning("All data cleared.")
        st.rerun()
