import streamlit as st
from graphviz import Digraph
import base64
import uuid

# Initialize session state
if "members" not in st.session_state:
    st.session_state.members = []
if "images" not in st.session_state:
    st.session_state.images = {}

st.title("👨‍👩‍👧‍👦 Interactive Family Tree Builder")

st.subheader("➕ Add a Family Member")
with st.form("add_member_form"):
    name = st.text_input("Full Name")
    dob = st.date_input("Date of Birth")
    parent = st.selectbox("Select Parent (if any)", ["None"] + [m["name"] for m in st.session_state.members])
    uploaded_image = st.file_uploader("Upload Photo (Optional)", type=["jpg", "jpeg", "png"])
    submit = st.form_submit_button("Add Member")

if submit and name:
    member_id = str(uuid.uuid4())
    parent_id = None
    if parent != "None":
        parent_id = next((m["id"] for m in st.session_state.members if m["name"] == parent), None)
    image_data = None
    if uploaded_image:
        image_data = base64.b64encode(uploaded_image.read()).decode()
        st.session_state.images[member_id] = image_data

    st.session_state.members.append({
        "id": member_id,
        "name": name,
        "dob": str(dob),
        "parent_id": parent_id,
    })
    st.success(f"{name} added to the tree!")

st.subheader("🌳 Family Tree Visualization")
tree = Digraph()
for member in st.session_state.members:
    label = f'{member["name"]}\nDOB: {member["dob"]}'
    tree.node(member["id"], label)
    if member["parent_id"]:
        tree.edge(member["parent_id"], member["id"])
st.graphviz_chart(tree)

st.subheader("🧾 Member List")
for member in st.session_state.members:
    st.markdown(f"**{member['name']}** (DOB: {member['dob']})")
    if member["id"] in st.session_state.images:
        image_html = f'<img src="data:image/png;base64,{st.session_state.images[member["id"]]}" width="100"/>'
        st.markdown(image_html, unsafe_allow_html=True)
    st.markdown("---")
