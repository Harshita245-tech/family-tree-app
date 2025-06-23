import streamlit as st
from graphviz import Digraph
import uuid

st.set_page_config(page_title="Family Tree", layout="wide")
st.title("🔗 Clean Family Tree (with arrows labeled)")

if "members" not in st.session_state:
    st.session_state.members = []  # {id, name, spouse_id, parent_ids, relation_label_to_parents}

def get_member_by_name(name):
    for m in st.session_state.members:
        if m["name"].lower().strip() == name.lower().strip():
            return m
    return None

st.subheader("➕ Add Member")
with st.form("member_form"):
    name = st.text_input("Name (only name inside circle)")
    spouse = st.text_input("Spouse Name (optional)")
    parents = st.text_input("Parent Names (comma-separated if both)")
    relation_to_parents = st.text_input("Relation label to show on arrow (e.g., Son, Daughter, Husband)")
    submit = st.form_submit_button("Add Member")

if submit and name:
    member_id = str(uuid.uuid4())
    spouse_id = None

    if spouse:
        existing = get_member_by_name(spouse)
        if existing:
            spouse_id = existing["id"]
        else:
            spouse_id = str(uuid.uuid4())
            st.session_state.members.append({
                "id": spouse_id,
                "name": spouse,
                "spouse_id": member_id,
                "parent_ids": [],
                "relation_label_to_parents": ""
            })

    parent_ids = []
    if parents:
        for pname in [p.strip() for p in parents.split(",")]:
            p = get_member_by_name(pname)
            if p:
                parent_ids.append(p["id"])

    st.session_state.members.append({
        "id": member_id,
        "name": name,
        "spouse_id": spouse_id,
        "parent_ids": parent_ids,
        "relation_label_to_parents": relation_to_parents
    })
    st.success(f"{name} added successfully.")

# Draw Graphviz
st.subheader("🧬 Visual Tree (Only names in circles, relation on arrows)")
dot = Digraph("FamilyTree")
dot.attr(rankdir="TB", nodesep="0.5", ranksep="1")

# Add nodes
added = set()
for member in st.session_state.members:
    if member["id"] not in added:
        dot.node(member["id"], label=member["name"], shape="circle", style="filled", color="lightgrey")
        added.add(member["id"])

# Couples
for member in st.session_state.members:
    if member["spouse_id"]:
        marriage_node = f"{member['id']}_{member['spouse_id']}_marriage"
        dot.node(marriage_node, shape="point", width="0.01", label="", style="invis")
        dot.edge(member["id"], marriage_node, arrowhead="none", weight="10")
        dot.edge(member["spouse_id"], marriage_node, arrowhead="none", weight="10")

        # Children
        for child in st.session_state.members:
            if set(child["parent_ids"]) == set([member["id"], member["spouse_id"]]):
                label = child.get("relation_label_to_parents", "")
                dot.edge(marriage_node, child["id"], label=label)

# Single parent → child arrows
for member in st.session_state.members:
    if member["parent_ids"] and len(member["parent_ids"]) == 1:
        label = member.get("relation_label_to_parents", "")
        dot.edge(member["parent_ids"][0], member["id"], label=label)

st.graphviz_chart(dot, use_container_width=True)
