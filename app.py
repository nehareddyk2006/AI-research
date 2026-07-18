import streamlit as st
from src.extraction.pdf_reader import extract_pdf
from src.graphs.knowledge_graph import build_graph
import streamlit.components.v1 as components
from src.ai.analyzer import analyze_paper
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="ResearchWeaver AI",
    page_icon="📚",
    layout="wide",
)

st.title("📚 ResearchWeaver AI")
st.caption("Analyze research papers in seconds using AI.")

uploaded_file = st.file_uploader(
    "Upload a Research Paper",
    type=["pdf"],
)

if uploaded_file:

    paper = extract_pdf(uploaded_file)

    st.success("✅ Paper uploaded successfully!")

    st.divider()

    st.subheader("📄 Paper Information")

    col1, col2 = st.columns([2, 1])

    with col1:

        st.markdown(f"### {paper.get('title', 'Untitled Paper')}")

        st.write(f"**👤 Authors:** {paper.get('authors', 'Not Available')}")

        st.write(f"**📚 Journal:** {paper.get('journal', 'Unknown')}")

        st.write(f"**📅 Published:** {paper.get('year', 'Unknown')}")

        keywords = paper.get("keywords", [])

        if keywords:
            st.write("**🏷 Keywords**")
            st.write(", ".join(keywords))

    with col2:

        st.metric("📄 Pages", paper.get("pages", 0))
        st.metric("📝 Words", paper.get("word_count", 0))
        st.metric(
            "⏱ Reading Time",
            f"{paper.get('reading_time',0)} min"
        )

    with st.expander("📖 Abstract"):

        st.write(
            paper.get(
                "abstract",
                "Abstract not detected."
            )
        )

    with st.expander("👀 View Extracted Text"):

        st.text(
            paper.get(
                "text",
                ""
            )[:5000]
        )

    st.divider()

    tabs = st.tabs(
        [
            "📄 Analysis",
            "🧠 Knowledge Graph",
            "🔍 Gap Finder",
            "🧪 Experiment Planner",
            "💬 Chat",
        ]
    )

    with tabs[0]:

        with st.spinner("Analyzing paper..."):

            analysis = analyze_paper(
                paper.get("text", "")
            )

        st.success("Analysis Complete!")

        st.subheader("📄 Summary")
        st.write(analysis.get("summary", ""))

        st.subheader("🎯 Research Problem")
        st.write(analysis.get("research_problem", ""))

        st.subheader("🧪 Methodology")
        st.write(analysis.get("methodology", ""))

        st.subheader("📊 Datasets")

        datasets = analysis.get("datasets", [])

        if datasets:
            for item in datasets:
                st.write("•", item)
        else:
            st.info("Not mentioned.")

        st.subheader("🤖 Models")

        models = analysis.get("models", [])

        if models:
            for item in models:
                st.write("•", item)
        else:
            st.info("Not mentioned.")

        st.subheader("📈 Evaluation Metrics")

        metrics = analysis.get("evaluation_metrics", [])

        if metrics:
            for item in metrics:
                st.write("•", item)
        else:
            st.info("Not mentioned.")

        st.subheader("⚠️ Limitations")

        limitations = analysis.get("limitations", [])

        if limitations:
            for item in limitations:
                st.write("•", item)
        else:
            st.info("Not mentioned.")

        st.subheader("🚀 Future Work")

        future = analysis.get("future_work", [])

        if future:
            for item in future:
                st.write("•", item)
        else:
            st.info("Not mentioned.")

    
    with tabs[1]:

        graph = analysis["knowledge_graph"]

        build_graph(graph)

        components.html(
            open(
                "graph.html",
                encoding="utf-8"
            ).read(),
            height=900,
            scrolling=True,
    )

        with st.expander("View Graph Data"):

            st.json(graph)
    with tabs[2]:
        st.info("🚧 Coming Soon")

    with tabs[3]:
        st.info("🚧 Coming Soon")

    with tabs[4]:
        st.info("🚧 Coming Soon")