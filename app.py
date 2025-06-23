# app.py  ── streamlined, arrow-labelled, vertical-only family tree
import streamlit as st
from graphviz import Digraph
import uuid

st.set_page_config(page_title="Vertical Family Tree", layout="wide")
st.title("🌳  Vertical Family Tree Builder")

# ────────────────────────────────────────────────────────────────────────
# Session-state helpers
# ────────────────────────────────────────────────────────────────────────
if "members" not in st.session_state:
    st.session_state.members = []      # list of dicts
def find_by_name(n):
    return next((m for m in st.session_state.members
                 if m["name"].strip().lower() == n.strip().lower()), None)

# ────────────────────────────────────────────────────────────────────────
# Input form
# ────────────────────────────────────────────────────────────────────────
st.subheader("➕  Add a person")
with st.form("add"):
    name          = st.text_input("Name  (inside circle)")
    spouse_name   = st.text_input("Spouse name (optional)")
    parents_line  = st.text_input("Parent name(s) (comma-separated, optional)")
    edge_label    = st.text_input("Text to write on arrow *from parents ➞ this child*"
                                  "  (e.g. Daughter, Son)", value="")
    submitted = st.form_submit_button("Add / link")

if submitted and name:
    pid = str(uuid.uuid4())                       # this person’s id
    sid = None                                    # spouse id, maybe

    # ── create / link spouse first ──────────────────────────────────────
    if spouse_name:
        exist = find_by_name(spouse_name)
        if exist:
            sid = exist["id"]
        else:
            sid = str(uuid.uuid4())
            st.session_state.members.append(
                dict(id=sid, name=spouse_name, spouse_id=pid,
                     parent_ids=[], arrow_label="") )

    # ── translate parent names ➞ ids ────────────────────────────────────
    parent_ids = []
    if parents_line:
        for p in map(str.strip, parents_line.split(",")):
            match = find_by_name(p)
            if match:
                parent_ids.append(match["id"])

    # ── finally add the main person ─────────────────────────────────────
    st.session_state.members.append(
        dict(id=pid, name=name, spouse_id=sid,
             parent_ids=parent_ids, arrow_label=edge_label) )
    st.success(f"Added {name}")

# ────────────────────────────────────────────────────────────────────────
# Build Graphviz diagram
# ────────────────────────────────────────────────────────────────────────
dot = Digraph("family", format="png")
dot.attr(rankdir="TB", nodesep="0.50", ranksep="1.0",
         node=dict(shape="circle", style="filled", color="white",
                   fontname="Helvetica", fontsize="10"),
         edge=dict(arrowsize="0.7"))

# 1️⃣  add every person as a node
for m in st.session_state.members:
    dot.node(m["id"], m["name"])

# 2️⃣  draw spouse connectors + capture marriage node ids
marriage_nodes = {}
for m in st.session_state.members:
    if m["spouse_id"]:
        a, b = m["id"], m["spouse_id"]
        # always create one marriage node per *unordered* pair
        key = "-".join(sorted([a, b]))
        if key not in marriage_nodes:
            mid = f"mar_{key}"
            marriage_nodes[key] = mid
            dot.node(mid, label="", shape="point", width="0.01")
            dot.edge(a, mid, arrowhead="none", weight="10")
            dot.edge(b, mid, arrowhead="none", weight="10")

# 3️⃣  connect children ↓ from the correct node
for child in st.session_state.members:
    if len(child["parent_ids"]) == 2:               # couple ➞ child
        key = "-".join(sorted(child["parent_ids"]))
        mid = marriage_nodes.get(key)
        if mid:
            dot.edge(mid, child["id"], label=child["arrow_label"])
    elif len(child["parent_ids"]) == 1:             # single parent ➞ child
        dot.edge(child["parent_ids"][0], child["id"],
                 label=child["arrow_label"])

st.subheader("📊  Tree preview")
st.graphviz_chart(dot, use_container_width=True)

# optional data inspector
with st.expander("📋 Raw member list"):
    for m in st.session_state.members:
        st.write(m)
