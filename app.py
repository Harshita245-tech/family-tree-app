import streamlit as st
from graphviz import Digraph
import uuid

st.set_page_config(page_title="Family Tree", layout="wide")
st.title("👨‍👩‍👧‍👦 Custom Family Tree Builder")

# Initialize family data
if "members" not in st.session_state:
    st.session_state.members = []  # Each item: {id, name, relation, spouse_id, parent_ids}

def get_member_by_name(name):
    for m in st.session_state.members:
        if m["name"] == name:
            return m
    return None

# Form to add family member
st.subheader("➕ Add a Family Member")

with st.form("add_member_form"):
    name = st.text_input("Name")
    relation = st.text_input("Relation (e.g. Daughter, Son, Great Grandmother)")
    spouse_name = st.text_input("Spouse Name (optional)")
    parent_names = st.text_input("Parent(s) Name(s) (comma separated, if known)")
    submit = st.form_submit_button("Add Member")

if submit and name:
    member_id = str(uuid.uuid4())
    spouse_id = None

    # Add spouse if provided
    if spouse_name:
        existing_spouse = get_member_by_name(spouse_name)
        if existing_spouse:
            spouse_id = existing_spouse["id"]
        else:
            spouse_id = str(uuid.uuid4())
            st.session_state.members.append({
                "id": spouse_id,
                "name": spouse_name,
                "relation": "Spouse",
                "spouse_id": member_id,
                "parent_ids": [],
            })

    # Link parents
    parent_ids = []
    if parent_names:
        for pname in [p.strip() for p in parent_names.split(",")]:
            parent = get_member_by_name(pname)
            if parent:
                parent_ids.append(parent["id"])

    # Add primary member
    st.session_state.members.append({
        "id": member_id,
        "name": name,
        "relation": relation,
        "spouse_id": spouse_id,
        "parent_ids": parent_ids,
    })
    st.success(f"✅ Added {name} with relation '{relation}'")

# Draw the family tree
st.subheader("🌳 Family Tree Visualization")

dot = Digraph(comment="Family Tree", format="png")
dot.attr(rankdir="TB", size="10")

added = set()

for member in st.session_state.members:
    if member["id"] not in added:
        label = f'{member["name"]}\n({member["relation"]})'
        dot.node(member["id"], label)
        added.add(member["id"])

    # Add spouse node and couple connector
    if member.get("spouse_id"):
        spouse = next((m for m in st.session_state.members if m["id"] == member["spouse_id"]), None)
        if spouse and spouse["id"] not in added:
            label = f'{spouse["name"]}\n({spouse["relation"]})'
            dot.node(spouse["id"], label)
            added.add(spouse["id"])
        # Add invisible node to connect them on same level
        couple_node = f"{member['id']}_{spouse['id']}_marriage"
        dot.node(couple_node, shape="point", width="0.01", label="")
        dot.edge(member["id"], couple_node, arrowhead="none", weight="10")
        dot.edge(spouse["id"], couple_node, arrowhead="none", weight="10")

        # Connect children to marriage node
        for child in st.session_state.members:
            if set(child["parent_ids"]) == set([member["id"], spouse["id"]]):
                dot.edge(couple_node, child["id"])

    else:
        # If single parent
        for child in st.session_state.members:
            if child["parent_ids"] == [member["id"]]:
                dot.edge(member["id"], child["id"])

st.graphviz_chart(dot, use_container_width=True)

# Show the data table
with st.expander("📋 View Member Data"):
    for m in st.session_state.members:
        st.write(f"🧍 {m['name']} – {m['relation']}")
