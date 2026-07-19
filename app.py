import streamlit as st
import streamlit.components.v1 as components

from src.extraction.pdf_reader import extract_pdf
from src.ai.analyzer import analyze_paper
from src.graphs.knowledge_graph import build_graph
from src.rag.chunker import chunk_text
from src.rag.vector_store import create_vector_store
from src.rag.chatbot import ask_question

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="ResearchWeaver AI",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# CACHE
# ----------------------------

@st.cache_resource
def build_vector_store(text):
    chunks = chunk_text(text)
    return create_vector_store(chunks)


@st.cache_data(show_spinner=False)
def analyze(text):
    return analyze_paper(text)

# ----------------------------
# CUSTOM CSS
# ----------------------------

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.hero{
padding:35px;
border-radius:22px;
border:1px solid rgba(255,255,255,.08);
background:linear-gradient(135deg,#121212,#1b1b1b);
margin-bottom:30px;
}

.metric-card{
padding:20px;
border-radius:18px;
background:#181818;
border:1px solid rgba(255,255,255,.06);
text-align:center;
}

.paper-card{
padding:25px;
border-radius:20px;
background:#161616;
border:1px solid rgba(255,255,255,.06);
}

.section{
padding-top:10px;
padding-bottom:10px;
}

</style>
""",unsafe_allow_html=True)

# ----------------------------
# SIDEBAR
# ----------------------------

with st.sidebar:

    st.title(":material/auto_stories: ResearchWeaver AI")

    st.caption(
        "AI-powered workspace for understanding research papers."
    )

    st.divider()

    st.subheader(":material/tips_and_updates: Suggested Questions")

    st.caption("""
• Summarize this paper

• Explain the methodology

• What dataset was used?

• What are the limitations?

• Suggest future work

• Explain this paper simply
""")

    st.divider()

    st.subheader(":material/info: About")

    st.caption("""
ResearchWeaver AI helps researchers understand papers faster using AI-powered analysis, Knowledge Graphs and Retrieval-Augmented Generation.
""")

# ----------------------------
# HERO
# ----------------------------

st.markdown("""
<div class='hero'>

<h1>ResearchWeaver AI</h1>

<p style="font-size:18px;color:#B8B8B8;">
Understand research papers in minutes using AI-powered analysis,
knowledge graphs, research gap detection and conversational RAG.
</p>

</div>
""",unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Research Paper",
    type=["pdf"]
)

if uploaded_file is None:

    st.info("Upload a PDF research paper to begin analysis.")

    st.stop()

# ----------------------------
# LOAD PAPER
# ----------------------------

with st.spinner("Extracting paper..."):

    paper = extract_pdf(uploaded_file)

text = paper.get("text","")

vector_store = build_vector_store(text)

with st.spinner("Running AI analysis..."):

    analysis = analyze(text)

# ----------------------------
# SIDEBAR STATS
# ----------------------------

with st.sidebar:

    st.divider()

    st.subheader(":material/analytics: Paper Statistics")

    st.metric("Pages",paper.get("pages",0))

    st.metric("Words",paper.get("word_count",0))

    st.metric(
        "Reading Time",
        f"{paper.get('reading_time',0)} min"
    )

    st.divider()

    st.success("Paper Loaded")

# ----------------------------
# PAPER HERO
# ----------------------------

left,right = st.columns([3,1])

with left:

    st.markdown(f"""
<div class="paper-card">

<h2>{paper.get("title","Untitled Paper")}</h2>

<p style="color:#BBBBBB;">
{paper.get("authors","Unknown")}
</p>

<p>

<b>Journal</b> • {paper.get("journal","Unknown")}

<br>

<b>Published</b> • {paper.get("year","Unknown")}

</p>

</div>
""",unsafe_allow_html=True)

with right:

    st.metric("Pages",paper.get("pages",0))
    st.metric("Words",paper.get("word_count",0))
    st.metric(
        "Reading Time",
        f"{paper.get('reading_time',0)} min"
    )

keywords = paper.get("keywords",[])

if keywords:

    st.caption(
        " • ".join(keywords)
    )

with st.expander("Abstract"):

    st.write(
        paper.get(
            "abstract",
            "Abstract not available."
        )
    )

with st.expander("Extracted Text"):

    st.text(text[:5000])

tabs = st.tabs([
    ":material/description: Analysis",
    ":material/account_tree: Knowledge Graph",
    ":material/search: Research Gaps",
    ":material/science: Experiment Planner",
    ":material/chat: Chat"
])
# ============================================================
# ANALYSIS
# ============================================================

with tabs[0]:

    st.markdown("## Paper Analysis")
    st.caption("AI-generated understanding of the uploaded paper.")

    def section(title, content):
        st.markdown(f"### {title}")
        st.container(border=True).write(content)

    section(
        "Executive Summary",
        analysis.get("summary", "Not available.")
    )

    section(
        "Research Problem",
        analysis.get("research_problem", "Not available.")
    )

    section(
        "Methodology",
        analysis.get("methodology", "Not available.")
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Datasets")

        datasets = analysis.get("datasets", [])

        if datasets:
            st.container(border=True)

            for item in datasets:
                st.markdown(f"- {item}")

        else:
            st.info("No datasets identified.")

    with col2:

        st.markdown("### Models")

        models = analysis.get("models", [])

        if models:

            for item in models:
                st.markdown(f"- {item}")

        else:
            st.info("No models identified.")

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("### Evaluation Metrics")

        metrics = analysis.get("evaluation_metrics", [])

        if metrics:

            for item in metrics:
                st.markdown(f"- {item}")

        else:

            st.info("Not mentioned.")

    with c2:

        st.markdown("### Limitations")

        limitations = analysis.get("limitations", [])

        if limitations:

            for item in limitations:
                st.markdown(f"- {item}")

        else:

            st.info("Not mentioned.")

    st.markdown("---")

    st.markdown("### Future Work")

    future = analysis.get("future_work", [])

    if future:

        for item in future:
            st.markdown(f"- {item}")

    else:

        st.info("Not mentioned.")

# ============================================================
# KNOWLEDGE GRAPH
# ============================================================

with tabs[1]:

    st.markdown("## Knowledge Graph")

    st.caption(
        "Visual representation of important entities and relationships extracted from the paper."
    )

    graph = analysis["knowledge_graph"]

    build_graph(graph)

    components.html(
        open(
            "graph.html",
            encoding="utf-8"
        ).read(),
        height=850,
        scrolling=True,
    )

    with st.expander("Graph JSON"):

        st.json(graph)
        # ============================================================
# RESEARCH GAPS
# ============================================================

with tabs[2]:

    st.markdown("## Research Gap Finder")
    st.caption(
        "Potential research opportunities identified by the AI."
    )

    gaps = analysis.get("research_gaps", [])

    if not gaps:

        st.info("No research gaps identified.")

    else:

        for gap in gaps:

            difficulty = gap.get(
                "difficulty",
                "Unknown"
            )

            col1, col2 = st.columns(
                [5,1]
            )

            with col1:

                st.markdown(
                    f"### {gap.get('title','Untitled')}"
                )

            with col2:

                if difficulty == "Easy":
                    st.success(difficulty)

                elif difficulty == "Medium":
                    st.warning(difficulty)

                else:
                    st.error(difficulty)

            with st.container():

                st.markdown("**Description**")

                st.write(
                    gap.get(
                        "description",
                        ""
                    )
                )

                st.markdown("**Why does this gap exist?**")

                st.write(
                    gap.get(
                        "reason",
                        ""
                    )
                )

                st.markdown("**Suggested Future Direction**")

                st.write(
                    gap.get(
                        "future_direction",
                        ""
                    )
                )

            st.divider()


# ============================================================
# EXPERIMENT PLANNER
# ============================================================

with tabs[3]:

    st.markdown("## Experiment Planner")

    st.caption(
        "Suggested roadmap for extending the uploaded research."
    )

    plan = analysis.get(
        "experiment_plan",
        {}
    )

    if not plan:

        st.info(
            "No experiment plan generated."
        )

    else:

        cards = [

            (
                "Objective",
                plan.get(
                    "objective",
                    ""
                )
            ),

            (
                "Recommended Dataset",
                plan.get(
                    "dataset",
                    ""
                )
            ),

            (
                "Proposed Model",
                plan.get(
                    "proposed_model",
                    ""
                )
            ),

            (
                "Expected Results",
                plan.get(
                    "expected_results",
                    ""
                )
            )

        ]

        for title, value in cards:

            with st.container():

                st.markdown(
                    f"### {title}"
                )

                st.write(value)

                st.divider()

        st.markdown(
            "### Preprocessing"
        )

        preprocessing = plan.get(
            "preprocessing",
            []
        )

        if preprocessing:

            for step in preprocessing:

                st.markdown(
                    f"- {step}"
                )

        else:

            st.info(
                "Not specified."
            )

        st.markdown(
            "### Baseline Models"
        )

        baselines = plan.get(
            "baseline_models",
            []
        )

        if baselines:

            for model in baselines:

                st.markdown(
                    f"- {model}"
                )

        else:

            st.info(
                "Not specified."
            )

        st.markdown(
            "### Evaluation Metrics"
        )

        metrics = plan.get(
            "evaluation_metrics",
            []
        )

        if metrics:

            for metric in metrics:

                st.markdown(
                    f"- {metric}"
                )

        else:

            st.info(
                "Not specified."
            )


# ============================================================
# CHAT
# ============================================================

with tabs[4]:

    st.markdown(
        "## Chat with your Paper"
    )

    st.caption(
        "Ask questions grounded in the uploaded paper."
    )

    if "messages" not in st.session_state:

        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    prompt = st.chat_input(
        "Ask a question..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role":"user",
                "content":prompt
            }
        )

        with st.chat_message(
            "user"
        ):

            st.markdown(
                prompt
            )

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Thinking..."
            ):

                answer = ask_question(
                    vector_store,
                    prompt
                )

            st.markdown(
                answer
            )

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )