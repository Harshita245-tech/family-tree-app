import streamlit as st
import uuid
import json

st.set_page_config(page_title="Proper Family Tree", layout="wide")
st.title("👨‍👩‍👧 Proper Top-Down Family Tree Builder")

# Initialize tree data
if "family" not in st.session_state:
    st.session_state.family = {}  # {id: {"name", "spouse", "children": [ids]}}

# Utility: get all member names
def get_member_options():
    return ["(Root)"] + [data["name"] for data in st.session_state.family.values()]

# Add new member
st.subheader("➕ Add a Family Member")
with st.form("add_member"):
    name = st.text_input("Name")
    spouse = st.text_input("Spouse (optional)")
    parent = st.selectbox("This person is a child of...", get_member_options())
    submitted = st.form_submit_button("Add to Tree")

if submitted and name:
    person_id = str(uuid.uuid4())
    st.session_state.family[person_id] = {
        "name": name,
        "spouse": spouse.strip(),
        "children": []
    }

    # Add to parent's children list
    if parent != "(Root)":
        for pid, pdata in st.session_state.family.items():
            if pdata["name"] == parent:
                pdata["children"].append(person_id)
                break
    st.success(f"{name} added!")

# Build nested HTML recursively
def render_member(member_id):
    member = st.session_state.family[member_id]
    spouse_html = f'<div class="member spouse">{member["spouse"]}</div>' if member["spouse"] else ""
    person_block = f'''
        <div class="family-pair">
            <div class="member">{member["name"]}</div>
            {spouse_html}
        </div>
    '''

    children_html = ""
    if member["children"]:
        children_blocks = "".join([render_member(cid) for cid in member["children"]])
        children_html = f'<div class="children">{children_blocks}</div>'

    return f'<div class="generation">{person_block}{children_html}</div>'

# Find roots (those without parents)
all_children = {cid for m in st.session_state.family.values() for cid in m["children"]}
roots = [pid for pid in st.session_state.family if pid not in all_children]

# Inject CSS
st.markdown("""
    <style>
    .generation {
        text-align: center;
        margin: 20px auto;
    }
    .family-pair {
        display: inline-flex;
        gap: 20px;
        justify-content: center;
        margin-bottom: 10px;
    }
    .member {
        padding: 10px 15px;
        background-color: #e0f7fa;
        border-radius: 8px;
        font-weight: bold;
        border: 2px solid #00acc1;
        min-width: 100px;
    }
    .spouse {
        background-color: #ffe0b2;
        border-color: #fb8c00;
    }
    .children {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 40px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.subheader("🌳 Family Tree Output")
tree_html = "".join([render_member(rid) for rid in roots])
st.markdown(tree_html, unsafe_allow_html=True)

# Optional JSON viewer
with st.expander("📋 Raw Family Data"):
    st.json(st.session_state.family)
