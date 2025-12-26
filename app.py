import streamlit as st
from graph import build_graph

st.set_page_config(
    page_title="Multi-Agent Article Generator",
    layout="wide"
)

st.title("🧠 Multi-Agent Article Generator")
st.caption("Powered by LangGraph")

article_graph = build_graph()

topic = st.text_input(
    "Enter Article Topic",
    placeholder="e.g. Future of Multi-Agent AI Systems"
)

if st.button("Generate Article"):
    if not topic:
        st.warning("Please enter a topic")
    else:
        with st.spinner("Agents are collaborating..."):
            result = article_graph.invoke({"topic": topic})

        st.success("Article Generated Successfully!")
        st.markdown(result["final"])
