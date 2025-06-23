import streamlit as st
from graphviz import Digraph
import uuid

st.set_page_config(page_title="Vertical Family Tree", layout="wide")
st.title("🌳 Vertical Family Tree Builder")

# Initialize session state
if "members" not in st.session_state:
    st.session_state.members = []  # list of dicts

# Utility: find member by name
def find_by_name(n):
    return next((m for m in st.session_state.members
                 if m["name"].strip().lower() == n.strip().lower()), None)

# 🔽 Input form
st.subheader("➕ Add a person")
with st.form("add"):
    name = st.text_input("Name (inside circle)")
    spouse_name = st.text_input("Spouse name (optional)")
    parents_line = st.text_input("Parent name(s) (comma-separated, optional)")
    arrow_label = st.text_input("Text on arrow from parent(s) to this person (e.g., Son, Daughter)", value="")
    submit = st.form_submit_button("Add / Link")

if submit and name:
    pid = str(uuid.uuid4())  # Person's unique ID
    sid = None

    # 🔗 Add or link spouse
    if spouse_name:
        existing = find_by_name(spouse_name)
        if existing:
            sid = existing["id"]
        else:
            sid = str(uuid.uuid4())
            st.session_state.members.append({
                "id": sid,
                "name": spouse_name,
                "spouse_id": pid,
                "parent_ids": [],
                "arrow_label": ""
            })

    # 🧬 Link parents
    parent_ids = []
    if parents_line:
        for pname in map(str.strip, parents_line.split(",")):
            match = find_by_name(pname)
            if match:
                parent_ids.append(match["id"])

    # ✅ Add main person
    st.session_state.members.append({
        "id": pid,
        "name": name,
        "spouse_id": sid,
        "parent_ids": parent_ids,
        "arrow_label": arrow_label
    })
    st.success(f"{name} added.")

# 🖼️ Visualize with Graphviz
dot = Digraph("family", format="png")
dot.attr(rankdir="TB", nodesep="0.5", ranksep="1.0")
dot.node_attr.update(shape="circle", style="filled", color="white",
                     fontname="Helvetica", fontsize="10")
dot.edge_attr.update(arrowsize="0.7")

# 🔵 Add all person nodes
added = set()
for member in st.session_state.members:
    if member["id"] not in added:
        dot.node(member["id"], member["name"])
        added.add(member["id"])

# 🔗 Couple logic
marriage_nodes = {}
for member in st.session_state.members:
    if member["spouse_id"]:
        a, b = member["id"], member["spouse_id"]
        key = "-".join(sorted([a, b]))
        if key not in marriage_nodes:
            mid = f"mar_{key}"
            marriage_nodes[key] = mid
            dot.node(mid, label="", shape="point", width="0.01")
            dot.edge(a, mid, arrowhead="none", weight="10")
            dot.edge(b, mid, arrowhead="none", weight="10")

# 🔽 Parent-child arrows with labels
for child in st.session_state.members:
    if len(child["parent_ids"]) == 2:
        key = "-".join(sorted(child["parent_ids"]))
        mid = marriage_nodes.get(key)
        if mid:
            dot.edge(mid, child["id"], label=child.get("arrow_label", ""))
    elif len(child["parent_ids"]) == 1:
        dot.edge(child["parent_ids"][0], child["id"], label=child.get("arrow_label", ""))

# 📊 Show result
st.subheader("📊 Tree Output (clean top-down view)")
st.graphviz_chart(dot, use_container_width=True)

# Optional viewer
with st.expander("📋 Member List"):
    for m in st.session_state.members:
        st.write(m)
