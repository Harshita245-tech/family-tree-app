import streamlit as st
from graphviz import Digraph
import uuid

st.set_page_config(page_title="Family Tree", layout="wide")
st.title("🌳 Infinite Vertical Family Tree Builder")

# ─── Session State ─────────────────────────────
if "members" not in st.session_state:
    st.session_state.members = []  # list of {id, name, spouse_id, parent_ids, arrow_label}

def get_member_by_name(name):
    return next((m for m in st.session_state.members
                 if m["name"].strip().lower() == name.strip().lower()), None)

# ─── Input Form ────────────────────────────────
st.subheader("➕ Add a Family Member")
with st.form("add_member"):
    name = st.text_input("Full Name (in circle)")
    spouse = st.text_input("Spouse Name (optional)")
    parent_names = st.text_input("Parent Name(s), comma separated (optional)")
    arrow_label = st.text_input("Text on arrow from parents to this person (optional)", placeholder="Daughter, Son, etc.")
    submit = st.form_submit_button("Add Member")

if submit and name:
    pid = str(uuid.uuid4())
    sid = None

    # Handle spouse
    if spouse:
        existing_spouse = get_member_by_name(spouse)
        if existing_spouse:
            sid = existing_spouse["id"]
        else:
            sid = str(uuid.uuid4())
            st.session_state.members.append({
                "id": sid,
                "name": spouse,
                "spouse_id": pid,
                "parent_ids": [],
                "arrow_label": ""
            })

    # Handle parents
    parent_ids = []
    if parent_names:
        for pname in map(str.strip, parent_names.split(",")):
            p = get_member_by_name(pname)
            if p:
                parent_ids.append(p["id"])

    # Add main person
    st.session_state.members.append({
        "id": pid,
        "name": name,
        "spouse_id": sid,
        "parent_ids": parent_ids,
        "arrow_label": arrow_label
    })
    st.success(f"{name} added successfully.")

# ─── Draw the Tree ─────────────────────────────
dot = Digraph("FamilyTree", format="png")
dot.attr(rankdir="TB", nodesep="0.5", ranksep="1.0")
dot.node_attr.update(shape="circle", style="filled", color="white",
                     fontname="Helvetica", fontsize="10")
dot.edge_attr.update(arrowsize="0.7")

# Add all people
added = set()
for person in st.session_state.members:
    if person["id"] not in added:
        dot.node(person["id"], person["name"])
        added.add(person["id"])

# Add marriage connectors
marriage_nodes = {}
for person in st.session_state.members:
    if person.get("spouse_id"):
        a, b = person["id"], person["spouse_id"]
        key = "-".join(sorted([a, b]))
        if key not in marriage_nodes:
            mid = f"marriage_{key}"
            marriage_nodes[key] = mid
            dot.node(mid, label="", shape="point", width="0.01")
            dot.edge(a, mid, arrowhead="none", weight="10")
            dot.edge(b, mid, arrowhead="none", weight="10")

# Connect children
for child in st.session_state.members:
    if len(child["parent_ids"]) == 2:
        key = "-".join(sorted(child["parent_ids"]))
        mid = marriage_nodes.get(key)
        if mid:
            dot.edge(mid, child["id"], label=child["arrow_label"])
    elif len(child["parent_ids"]) == 1:
        dot.edge(child["parent_ids"][0], child["id"], label=child["arrow_label"])

# ─── Render ─────────────────────────────
st.subheader("📊 Family Tree Output")
st.graphviz_chart(dot, use_container_width=True)

# Optional raw data
with st.expander("📋 Member List"):
    for m in st.session_state.members:
        st.write(m)
