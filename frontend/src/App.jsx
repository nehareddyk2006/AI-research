import { useMemo, useState } from "react";
import {
  Upload,
  FileText,
  Sparkles,
  ArrowRight,
  BookOpen,
  Clock3,
  Hash,
  Users,
  Database,
  BrainCircuit,
  Target,
  FlaskConical,
  Network,
  Search,
  MessageSquare,
  ChevronDown,
  AlertTriangle,
  Lightbulb,
  CheckCircle2,
  Loader2,
} from "lucide-react";

import {
  analyzePaper,
  askPaper,
} from "./api";


function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFile = async (selectedFile) => {
    if (!selectedFile) return;

    if (
      selectedFile.type !== "application/pdf" &&
      !selectedFile.name.toLowerCase().endsWith(".pdf")
    ) {
      setError("Please upload a PDF research paper.");
      return;
    }

    setFile(selectedFile);
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const data = await analyzePaper(selectedFile);
      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Something went wrong while analyzing the paper."
      );
      setResult(null);
    } finally {
      setLoading(false);
    }
  };


  const handleDrop = (event) => {
    event.preventDefault();

    const droppedFile =
      event.dataTransfer.files?.[0];

    handleFile(droppedFile);
  };


  const handleInput = (event) => {
    const selectedFile =
      event.target.files?.[0];

    handleFile(selectedFile);
  };


  const reset = () => {
    setFile(null);
    setResult(null);
    setError("");
    setLoading(false);
  };


  return (
    <div className="app-shell">

      {/* ================= HEADER ================= */}

      <header className="topbar">

        <div className="brand">

          <div className="brand-mark">
            <Sparkles size={18} />
          </div>

          <span>ResearchWeaver</span>

        </div>

        <div className="topbar-status">
          <span className="status-dot" />
          AI Research Workspace
        </div>

      </header>


      {/* ================= LANDING PAGE ================= */}

      {!result && !loading && (

        <main className="hero-page">

          <section className="hero">

            <div className="hero-eyebrow">
              <Sparkles size={15} />
              Research intelligence workspace
            </div>


            <h1>
              Turn research papers into
              <span> actionable intelligence.</span>
            </h1>


            <p className="hero-description">
              Upload a research paper and let ResearchWeaver
              uncover its methodology, datasets, research gaps,
              experiment opportunities, and underlying knowledge.
            </p>


            {/* ================= UPLOAD ================= */}

            <div
              className="upload-zone"
              onDragOver={(event) =>
                event.preventDefault()
              }
              onDrop={handleDrop}
            >

              <div className="upload-icon">
                <Upload size={25} />
              </div>


              <h3>
                Drop your research paper here
              </h3>


              <p>
                PDF files only · AI-powered analysis
              </p>


              <label className="primary-button">

                Browse files

                <ArrowRight size={16} />

                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={handleInput}
                  hidden
                />

              </label>

            </div>


            {/* ================= ERROR ================= */}

            {error && (

              <div className="error-message">

                <AlertTriangle size={17} />

                {error}

              </div>

            )}


            {/* ================= FEATURES ================= */}

            <div className="feature-grid">

              <FeatureCard
                icon={<BookOpen size={19} />}
                title="Paper Analysis"
                description="Extract the core research question, methodology, datasets, and findings."
              />


              <FeatureCard
                icon={<Search size={19} />}
                title="Gap Finder"
                description="Identify unexplored directions and potential research opportunities."
              />


              <FeatureCard
                icon={<FlaskConical size={19} />}
                title="Experiment Planner"
                description="Turn research gaps into structured experimental ideas."
              />

            </div>

          </section>

        </main>

      )}


      {/* ================= LOADING ================= */}

      {loading && (
        <LoadingScreen file={file} />
      )}


      {/* ================= DASHBOARD ================= */}

      {result && !loading && (

        <ResearchDashboard
          result={result}
          file={file}
          onReset={reset}
        />

      )}

    </div>
  );
}


/* =========================================================
   FEATURE CARD
========================================================= */

function FeatureCard({
  icon,
  title,
  description,
}) {

  return (

    <div className="feature-card">

      <div className="feature-icon">
        {icon}
      </div>

      <div>

        <h3>{title}</h3>

        <p>{description}</p>

      </div>

    </div>

  );
}


/* =========================================================
   LOADING SCREEN
========================================================= */

function LoadingScreen({ file }) {

  return (

    <main className="loading-page">

      <div className="loading-card">

        <div className="loading-icon">

          <Loader2
            size={30}
            className="spin"
          />

        </div>


        <h2>
          Reading your research
        </h2>


        <p>
          ResearchWeaver is extracting the paper,
          understanding its structure, and generating
          research intelligence.
        </p>


        {file && (

          <div className="file-preview">

            <FileText size={18} />

            <div>

              <strong>
                {file.name}
              </strong>

              <span>
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </span>

            </div>

          </div>

        )}


        <div className="loading-bar">
          <div />
        </div>

      </div>

    </main>

  );
}


/* =========================================================
   DASHBOARD
========================================================= */

function ResearchDashboard({
  result,
  file,
  onReset,
}) {

  const paper =
    result?.paper || {};

  const analysis =
    result?.analysis || {};


  return (

    <main className="dashboard">

      {/* ================= DASHBOARD HEADER ================= */}

      <section className="dashboard-header">

        <div>

          <button
            className="back-button"
            onClick={onReset}
          >

            <ArrowRight
              size={15}
              className="back-arrow"
            />

            Analyze another paper

          </button>


          <div className="paper-label">

            <FileText size={15} />

            Research paper

          </div>


          <h1>
            {paper.title || "Untitled Paper"}
          </h1>


          <p className="paper-authors">

            {paper.authors ||
              "Authors unavailable"}

          </p>

        </div>


        <div className="analysis-status">

          <CheckCircle2 size={17} />

          Analysis complete

        </div>

      </section>


      {/* ================= STATS ================= */}

      <section className="stats-grid">

        <StatCard
          icon={<FileText size={18} />}
          label="Pages"
          value={paper.pages || 0}
        />


        <StatCard
          icon={<Hash size={18} />}
          label="Words"
          value={
            (paper.word_count || 0)
              .toLocaleString()
          }
        />


        <StatCard
          icon={<Clock3 size={18} />}
          label="Reading time"
          value={`${paper.reading_time || 0} min`}
        />


        <StatCard
          icon={<BookOpen size={18} />}
          label="Published"
          value={paper.year || "Unknown"}
        />

      </section>


      {/* ================= MAIN CONTENT ================= */}

      <section className="content-grid">

        <div className="main-column">

          <SectionCard
            icon={<Sparkles size={18} />}
            title="Executive Summary"
          >

            <p className="large-copy">

              {analysis.summary ||
                "No summary was generated."}

            </p>

          </SectionCard>


          <SectionCard
            icon={<Target size={18} />}
            title="Research Problem"
          >

            <p>

              {analysis.research_problem ||
                "Not identified in the paper."}

            </p>

          </SectionCard>


          <SectionCard
            icon={<BrainCircuit size={18} />}
            title="Methodology"
          >

            <p>

              {analysis.methodology ||
                "Not identified in the paper."}

            </p>

          </SectionCard>


          <ListSection
            icon={<Database size={18} />}
            title="Datasets"
            items={analysis.datasets}
          />


          <ListSection
            icon={<BrainCircuit size={18} />}
            title="Models"
            items={analysis.models}
          />


          <ListSection
            icon={<Target size={18} />}
            title="Evaluation Metrics"
            items={analysis.evaluation_metrics}
          />


          <div className="two-column">

            <ListSection
              icon={<AlertTriangle size={18} />}
              title="Limitations"
              items={analysis.limitations}
            />


            <ListSection
              icon={<Lightbulb size={18} />}
              title="Future Work"
              items={analysis.future_work}
            />

          </div>

        </div>


        {/* ================= SIDEBAR ================= */}

        <aside className="side-column">

          <MetadataCard
            paper={paper}
          />


          <KeywordsCard
            keywords={paper.keywords}
          />


          <AbstractCard
            abstract={paper.abstract}
          />

        </aside>

      </section>


      {/* ================= RESEARCH GAPS ================= */}

      <ResearchGaps
        gaps={analysis.research_gaps}
      />


      {/* ================= EXPERIMENT PLANNER ================= */}

      <ExperimentPlanner
        plan={analysis.experiment_plan}
      />


      {/* ================= KNOWLEDGE GRAPH ================= */}

      <KnowledgeGraph
        graph={analysis.knowledge_graph}
      />


      {/* ================= CHAT ================= */}

      <PaperChat
        file={file}
      />

    </main>

  );
}


/* =========================================================
   STAT CARD
========================================================= */

function StatCard({
  icon,
  label,
  value,
}) {

  return (

    <div className="stat-card">

      <div className="stat-icon">
        {icon}
      </div>

      <div>

        <span>{label}</span>

        <strong>{value}</strong>

      </div>

    </div>

  );

}


/* =========================================================
   SECTION CARD
========================================================= */

function SectionCard({
  icon,
  title,
  children,
}) {

  return (

    <section className="section-card">

      <div className="section-heading">

        <div className="section-heading-icon">
          {icon}
        </div>

        <h2>{title}</h2>

      </div>

      {children}

    </section>

  );

}


/* =========================================================
   LIST SECTION
========================================================= */

function ListSection({
  icon,
  title,
  items = [],
}) {

  return (

    <SectionCard
      icon={icon}
      title={title}
    >

      {items?.length ? (

        <div className="item-list">

          {items.map((item, index) => (

            <div
              className="list-item"
              key={index}
            >

              <span className="list-number">
                {String(index + 1).padStart(2, "0")}
              </span>

              <span>
                {item}
              </span>

            </div>

          ))}

        </div>

      ) : (

        <p className="muted">
          Not identified in the paper.
        </p>

      )}

    </SectionCard>

  );

}


/* =========================================================
   METADATA
========================================================= */

function MetadataCard({ paper }) {

  return (

    <div className="side-card">

      <div className="side-card-heading">

        <Users size={17} />

        <span>
          Paper details
        </span>

      </div>


      <div className="metadata">

        <div>

          <span>
            Authors
          </span>

          <strong>
            {paper.authors ||
              "Unavailable"}
          </strong>

        </div>


        <div>

          <span>
            Journal
          </span>

          <strong>
            {paper.journal ||
              "Unknown"}
          </strong>

        </div>


        <div>

          <span>
            Publication year
          </span>

          <strong>
            {paper.year ||
              "Unknown"}
          </strong>

        </div>

      </div>

    </div>

  );

}


/* =========================================================
   KEYWORDS
========================================================= */

function KeywordsCard({
  keywords = [],
}) {

  return (

    <div className="side-card">

      <div className="side-card-heading">

        <Hash size={17} />

        <span>
          Keywords
        </span>

      </div>


      <div className="keyword-list">

        {keywords?.length ? (

          keywords.map(
            (keyword, index) => (

              <span key={index}>
                {keyword}
              </span>

            )
          )

        ) : (

          <span className="muted">
            No keywords detected.
          </span>

        )}

      </div>

    </div>

  );

}


/* =========================================================
   ABSTRACT
========================================================= */

function AbstractCard({
  abstract,
}) {

  return (

    <details className="side-card expandable-card">

      <summary>

        <BookOpen size={17} />

        <span>
          Abstract
        </span>

        <ChevronDown size={16} />

      </summary>


      <p>

        {abstract ||
          "Abstract not detected."}

      </p>

    </details>

  );

}


/* =========================================================
   RESEARCH GAPS
========================================================= */

function ResearchGaps({
  gaps = [],
}) {

  return (

    <section className="wide-section">

      <SectionHeader
        icon={<Search size={20} />}
        eyebrow="Research intelligence"
        title="Research Gap Finder"
        description="Potential directions identified from the paper."
      />


      {gaps?.length ? (

        <div className="gap-grid">

          {gaps.map(
            (gap, index) => (

              <div
                className="gap-card"
                key={index}
              >

                <div className="gap-top">

                  <span className="gap-number">
                    {String(index + 1).padStart(2, "0")}
                  </span>

                  <Difficulty
                    value={gap.difficulty}
                  />

                </div>


                <h3>
                  {gap.title ||
                    "Research gap"}
                </h3>


                <p>
                  {gap.description ||
                    "No description provided."}
                </p>


                <details>

                  <summary>

                    Why does this gap exist?

                    <ChevronDown size={15} />

                  </summary>


                  <p>
                    {gap.reason ||
                      "No reason provided."}
                  </p>

                </details>


                <div className="direction">

                  <Lightbulb size={16} />

                  <div>

                    <span>
                      Future direction
                    </span>

                    <p>
                      {gap.future_direction ||
                        "No future direction provided."}
                    </p>

                  </div>

                </div>

              </div>

            )
          )}

        </div>

      ) : (

        <EmptyState
          text="No research gaps were identified."
        />

      )}

    </section>

  );

}


/* =========================================================
   DIFFICULTY
========================================================= */

function Difficulty({ value }) {

  const difficulty =
    value || "Unknown";


  return (

    <span
      className={`difficulty ${difficulty.toLowerCase()}`}
    >

      {difficulty}

    </span>

  );

}


/* =========================================================
   EXPERIMENT PLANNER
========================================================= */

function ExperimentPlanner({
  plan,
}) {

  if (!plan) return null;


  return (

    <section className="wide-section">

      <SectionHeader
        icon={<FlaskConical size={20} />}
        eyebrow="Research intelligence"
        title="Experiment Planner"
        description="A structured path from research gap to experiment."
      />


      <div className="experiment-grid">

        <div className="experiment-objective">

          <span>
            Objective
          </span>

          <h3>
            {plan.objective ||
              "No objective generated."}
          </h3>

        </div>


        <ExperimentBlock
          title="Recommended dataset"
          content={plan.dataset}
        />


        <ExperimentList
          title="Preprocessing"
          items={plan.preprocessing}
        />


        <ExperimentList
          title="Baseline models"
          items={plan.baseline_models}
        />


        <div className="proposed-model">

          <span>
            Proposed improved model
          </span>

          <h3>
            {plan.proposed_model ||
              "Not specified."}
          </h3>

        </div>


        <ExperimentList
          title="Evaluation metrics"
          items={plan.evaluation_metrics}
        />


        <ExperimentBlock
          title="Expected results"
          content={plan.expected_results}
        />

      </div>

    </section>

  );

}


/* =========================================================
   EXPERIMENT BLOCK
========================================================= */

function ExperimentBlock({
  title,
  content,
}) {

  return (

    <div className="experiment-block">

      <span>
        {title}
      </span>

      <p>
        {content ||
          "Not specified."}
      </p>

    </div>

  );

}


/* =========================================================
   EXPERIMENT LIST
========================================================= */

function ExperimentList({
  title,
  items = [],
}) {

  return (

    <div className="experiment-block">

      <span>
        {title}
      </span>


      {items?.length ? (

        <ul>

          {items.map(
            (item, index) => (

              <li key={index}>
                {item}
              </li>

            )
          )}

        </ul>

      ) : (

        <p>
          Not specified.
        </p>

      )}

    </div>

  );

}


/* =========================================================
   KNOWLEDGE GRAPH
========================================================= */

function getNodeColor(type) {
  const normalizedType = String(type || "Concept").trim().toLowerCase();

  const palette = {
    model: "#6366F1",
    method: "#10B981",
    dataset: "#F59E0B",
    metric: "#EF4444",
    concept: "#8B5CF6",
    domain: "#06B6D4",
    task: "#EC4899",
    problem: "#DC2626",
    technique: "#14B8A6",
    application: "#F97316",
    unknown: "#94A3B8",
  };

  return palette[normalizedType] || "#94A3B8";
}

function wrapText(text, maxChars) {
  const safeText = String(text || "Unknown");
  const words = safeText.split(/\s+/);
  const lines = [];
  let currentLine = "";

  words.forEach((word) => {
    const candidate = currentLine ? `${currentLine} ${word}` : word;

    if (candidate.length <= maxChars) {
      currentLine = candidate;
      return;
    }

    if (currentLine) {
      lines.push(currentLine);
    }

    if (word.length > maxChars) {
      const chunk = word.slice(0, maxChars);
      lines.push(chunk);
      currentLine = word.slice(maxChars);
      return;
    }

    currentLine = word;
  });

  if (currentLine) {
    lines.push(currentLine);
  }

  return lines.slice(0, 3);
}

function normalizeKnowledgeGraph(graph) {
  const rawNodes = Array.isArray(graph?.nodes) ? graph.nodes : [];
  const rawEdges = Array.isArray(graph?.edges) ? graph.edges : [];

  const nodeMap = new Map();

  rawNodes.forEach((node) => {
    if (!node || node.id == null) return;

    const id = String(node.id);
    if (nodeMap.has(id)) return;

    nodeMap.set(id, {
      id,
      label: String(node.label || node.name || id),
      type: String(node.type || "Concept").trim() || "Concept",
    });
  });

  const nodeIds = new Set(nodeMap.keys());
  const dedupedEdges = new Set();

  const edges = rawEdges.reduce((acc, edge) => {
    if (!edge || edge.source == null || edge.target == null) return acc;

    const source = String(edge.source);
    const target = String(edge.target);

    if (
      source === target ||
      !nodeIds.has(source) ||
      !nodeIds.has(target)
    ) {
      return acc;
    }

    const relation = String(edge.relation || "related to");
    const key = `${source}->${target}:${relation}`;
    if (dedupedEdges.has(key)) return acc;

    dedupedEdges.add(key);
    acc.push({ source, target, relation });
    return acc;
  }, []);

  const nodes = Array.from(nodeMap.values()).map((node) => ({
    ...node,
    type: node.type || "Concept",
    connectionCount: edges.filter(
      (edge) => edge.source === node.id || edge.target === node.id
    ).length,
  }));

  return { nodes, edges };
}

function buildMindMapLayout(nodes, edges, width, height) {
  if (!nodes.length) {
    return { positions: new Map(), rootId: null };
  }

  const adjacency = new Map();
  const nodeMap = new Map(nodes.map((node) => [node.id, node]));

  nodes.forEach((node) => adjacency.set(node.id, []));

  edges.forEach((edge) => {
    if (!nodeMap.has(edge.source) || !nodeMap.has(edge.target)) return;
    adjacency.get(edge.source).push(edge.target);
    adjacency.get(edge.target).push(edge.source);
  });

  const degree = (nodeId) => adjacency.get(nodeId)?.length || 0;
  const rootId = [...nodeMap.keys()].sort(
    (left, right) =>
      degree(right) - degree(left) ||
      nodeMap.get(left).label.localeCompare(nodeMap.get(right).label)
  )[0];

  const positions = new Map();
  positions.set(rootId, { x: width / 2, y: height / 2 });

  const queue = [{ id: rootId, parentId: null, depth: 0, angle: 0 }];
  const visited = new Set([rootId]);

  while (queue.length > 0) {
    const current = queue.shift();
    const currentPos = positions.get(current.id);
    const children = (adjacency.get(current.id) || [])
      .filter((childId) => childId !== current.parentId && !visited.has(childId))
      .sort((left, right) => {
        const leftNode = nodeMap.get(left);
        const rightNode = nodeMap.get(right);
        return (
          degree(right) - degree(left) ||
          leftNode.label.localeCompare(rightNode.label)
        );
      });

    if (!children.length) continue;

    const rootSpread = current.depth === 0 ? Math.PI * 2 : Math.PI * 0.9;
    const startAngle = current.depth === 0 ? -Math.PI : current.angle - rootSpread / 2;
    const branchSpacing = rootSpread / Math.max(children.length, 1);

    children.forEach((childId, index) => {
      const childAngle =
        current.depth === 0
          ? startAngle + branchSpacing * (index + 0.5)
          : current.angle + (index - (children.length - 1) / 2) * 0.9;

      const distance = 150 + current.depth * 100 + (children.length > 3 ? 35 : 0);
      const x = currentPos.x + Math.cos(childAngle) * distance;
      const y = currentPos.y + Math.sin(childAngle) * distance;

      positions.set(childId, { x, y });
      visited.add(childId);
      queue.push({
        id: childId,
        parentId: current.id,
        depth: current.depth + 1,
        angle: childAngle,
      });
    });
  }

  const remainingNodes = nodes.filter((node) => !positions.has(node.id));

  remainingNodes.forEach((node, index) => {
    const angle = (index / Math.max(remainingNodes.length, 1)) * Math.PI * 2;
    const orbit = 120 + index * 16;
    positions.set(node.id, {
      x: width / 2 + Math.cos(angle) * orbit,
      y: height / 2 + Math.sin(angle) * orbit,
    });
  });

  return { positions, rootId };
}

function KnowledgeGraph({ graph }) {
  const normalizedGraph = useMemo(
    () => normalizeKnowledgeGraph(graph),
    [graph]
  );

  const nodes = normalizedGraph.nodes;
  const edges = normalizedGraph.edges;

  const [selectedNode, setSelectedNode] = useState(null);
  const [hoveredNode, setHoveredNode] = useState(null);

  const width = 900;
  const height = 540;
  const layout = useMemo(
    () => buildMindMapLayout(nodes, edges, width, height),
    [nodes, edges]
  );

  const positions = layout.positions;
  const selectedNodeId = selectedNode?.id;
  const relatedNodeIds = new Set(selectedNodeId ? [selectedNodeId] : []);

  if (selectedNodeId) {
    edges.forEach((edge) => {
      if (edge.source === selectedNodeId) relatedNodeIds.add(edge.target);
      if (edge.target === selectedNodeId) relatedNodeIds.add(edge.source);
    });
  }

  if (!nodes.length) {
    return (
      <section className="wide-section">
        <SectionHeader
          icon={<Network size={20} />}
          eyebrow="Research intelligence"
          title="Knowledge Graph"
          description="A visual map of concepts and relationships extracted from the paper."
        />

        <div className="graph-card">
          <div className="graph-empty">
            <Network size={40} />

            <h3>No knowledge graph generated</h3>

            <p>
              No concepts or relationships were detected in this paper.
            </p>
          </div>
        </div>
      </section>
    );
  }

  const hoveredPosition = hoveredNode
    ? positions.get(hoveredNode.id)
    : null;

  const rootId = layout.rootId || nodes[0]?.id;

  const nodeEntries = nodes.map((node) => {
    const key = node.id;
    const position = positions.get(key) || { x: width / 2, y: height / 2 };
    const labelLines = wrapText(node.label || node.id, 18);
    const nodeWidth = Math.min(200, Math.max(140, 110 + (node.label?.length || 0) * 2.6));
    const lineHeight = 15;
    const cardHeight = 28 + labelLines.length * lineHeight + 18;
    const x = position.x;
    const y = position.y;

    const isSelected = selectedNode?.id === node.id;
    const isHovered = hoveredNode?.id === node.id;
    const isDimmed = selectedNodeId && !relatedNodeIds.has(node.id);

    return {
      ...node,
      key,
      x,
      y,
      nodeWidth,
      cardHeight,
      isSelected,
      isHovered,
      isDimmed,
      labelLines,
    };
  });

  const connectedRelations = selectedNode
    ? edges
        .filter(
          (edge) =>
            edge.source === selectedNode.id || edge.target === selectedNode.id
        )
        .map((edge) => {
          const connectedId =
            edge.source === selectedNode.id ? edge.target : edge.source;
          const connectedLabel =
            nodes.find((node) => node.id === connectedId)?.label || connectedId;

          return {
            id: `${selectedNode.id}-${connectedId}-${edge.relation}`,
            relation: edge.relation || "related to",
            connectedId,
            connectedLabel,
          };
        })
    : [];

  return (
    <section className="wide-section">
      <SectionHeader
        icon={<Network size={20} />}
        eyebrow="Research intelligence"
        title="Knowledge Graph"
        description="A structured map of concepts, methods, datasets, and problems extracted from the paper."
      />

      <div className="knowledge-graph">
        <div className="graph-toolbar">
          <div className="graph-count">
            <strong>{nodes.length}</strong>
            <span>concepts</span>
            <span className="graph-divider">/</span>
            <strong>{edges.length}</strong>
            <span>relationships</span>
          </div>

          <span className="graph-hint">
            Hover for details · Click to inspect
          </span>
        </div>

        <div className="graph-container">
          <svg
            className="graph-svg"
            viewBox={`0 0 ${width} ${height}`}
            preserveAspectRatio="xMidYMid meet"
            aria-label="Knowledge graph"
          >
            <defs>
              <marker
                id="arrowhead"
                markerWidth="8"
                markerHeight="8"
                refX="7"
                refY="3.5"
                orient="auto"
              >
                <path d="M0,0 L0,7 L7,3.5 z" fill="rgba(255,255,255,0.45)" />
              </marker>
            </defs>

            {edges.map((edge, index) => {
              const source = positions.get(edge.source) || { x: width / 2, y: height / 2 };
              const target = positions.get(edge.target) || { x: width / 2, y: height / 2 };
              const sourceNode = nodes.find((node) => node.id === edge.source);
              const showEdge =
                !selectedNodeId ||
                edge.source === selectedNodeId ||
                edge.target === selectedNodeId;

              const baseOpacity = showEdge ? 0.9 : 0.18;
              const strokeColor = selectedNodeId
                ? showEdge
                  ? "rgba(255,255,255,0.75)"
                  : "rgba(255,255,255,0.1)"
                : "rgba(255,255,255,0.42)";

              const dx = target.x - source.x;
              const dy = target.y - source.y;
              const controlOffsetX = dx * 0.42;
              const controlOffsetY = dy * 0.42;

              const path = `M ${source.x} ${source.y} C ${source.x + controlOffsetX} ${source.y + controlOffsetY}, ${target.x - controlOffsetX} ${target.y - controlOffsetY}, ${target.x} ${target.y}`;

              return (
                <g key={`${edge.source}-${edge.target}-${edge.relation}-${index}`}>
                  <path
                    d={path}
                    fill="none"
                    stroke={strokeColor}
                    strokeWidth={selectedNodeId ? (showEdge ? 1.8 : 0.7) : 1.3}
                    strokeOpacity={baseOpacity}
                    markerEnd="url(#arrowhead)"
                    style={{ cursor: "pointer" }}
                    onMouseEnter={() => setHoveredNode(sourceNode || null)}
                    onMouseLeave={() => setHoveredNode(null)}
                  >
                    <title>{edge.relation || "related to"}</title>
                  </path>
                </g>
              );
            })}

            {nodeEntries.map((node) => {
              const left = node.x - node.nodeWidth / 2;
              const top = node.y - node.cardHeight / 2;
              const isHighlighted =
                node.isSelected || node.isHovered || (!selectedNodeId && rootId === node.id);
              const opacity = selectedNodeId && node.isDimmed ? 0.25 : 1;

              return (
                <g
                  key={node.id}
                  className={`graph-node ${node.isSelected ? "selected" : ""} ${node.isHovered ? "hovered" : ""}`}
                  style={{ opacity, cursor: "pointer" }}
                  onMouseEnter={() => setHoveredNode({ id: node.id, label: node.label, type: node.type })}
                  onMouseLeave={() => setHoveredNode(null)}
                  onClick={() => setSelectedNode({ id: node.id, label: node.label, type: node.type })}
                >
                  <rect
                    x={left}
                    y={top}
                    width={node.nodeWidth}
                    height={node.cardHeight}
                    rx={14}
                    fill="rgba(17, 17, 17, 0.94)"
                    stroke={isHighlighted ? "rgba(255,255,255,0.9)" : `${getNodeColor(node.type)}99`}
                    strokeWidth={isHighlighted ? 2.1 : 1.2}
                  />

                  <text
                    x={node.x}
                    y={top + 20}
                    textAnchor="middle"
                    fill="#f8fafc"
                    fontSize="12"
                    fontWeight="600"
                    style={{ pointerEvents: "none" }}
                  >
                    {node.labelLines.map((line, index) => (
                      <tspan key={`${node.id}-${line}`} x={node.x} dy={index === 0 ? 0 : 15}>
                        {line}
                      </tspan>
                    ))}
                  </text>

                  <text
                    x={node.x}
                    y={top + node.cardHeight - 10}
                    textAnchor="middle"
                    fill="rgba(255,255,255,0.72)"
                    fontSize="10"
                    letterSpacing="0.08em"
                    style={{ textTransform: "uppercase", pointerEvents: "none" }}
                  >
                    {node.type}
                  </text>
                </g>
              );
            })}
          </svg>

          {hoveredPosition && hoveredNode && (
            <div
              className="graph-tooltip"
              style={{
                left: `${Math.min(hoveredPosition.x + 18, width - 150)}px`,
                top: `${Math.max(hoveredPosition.y - 28, 16)}px`,
              }}
            >
              <strong>{hoveredNode.label || hoveredNode.id}</strong>
              <span>{hoveredNode.type || "Concept"}</span>
            </div>
          )}

          {selectedNode && (
            <div className="graph-inspector">
              <button
                className="graph-inspector-close"
                onClick={() => setSelectedNode(null)}
              >
                ×
              </button>

              <span
                className="graph-inspector-type"
                style={{ color: getNodeColor(selectedNode.type) }}
              >
                {selectedNode.type || "Concept"}
              </span>

              <h3>{selectedNode.label || selectedNode.id}</h3>

              <div className="inspector-stat">
                <span>Connections</span>
                <strong>
                  {edges.filter(
                    (edge) =>
                      edge.source === selectedNode.id || edge.target === selectedNode.id
                  ).length}
                </strong>
              </div>

              <div className="inspector-relations">
                {connectedRelations.length ? (
                  connectedRelations.map((item) => (
                    <div className="inspector-relation" key={item.id}>
                      <span>{item.relation}</span>
                      <strong>{item.connectedLabel}</strong>
                    </div>
                  ))
                ) : (
                  <div className="inspector-relation">
                    <span>related to</span>
                    <strong>None</strong>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        <GraphLegend nodes={nodes} />
      </div>
    </section>
  );
}

function GraphLegend({ nodes }) {
  const types = [
    ...new Set(
      nodes
        .map((node) => node.type)
        .filter(Boolean)
    ),
  ];

  return (
    <div className="graph-legend">
      {types.map((type) => (
        <div
          className="graph-legend-item"
          key={type}
        >
          <span
            className="graph-legend-dot"
            style={{
              backgroundColor: getNodeColor(type),
            }}
          />

          <span>{type}</span>
        </div>
      ))}
    </div>
  );
}
/* =========================================================
   SECTION HEADER
========================================================= */

function SectionHeader({
  icon,
  eyebrow,
  title,
  description,
}) {

  return (

    <div className="wide-header">

      <div className="wide-icon">
        {icon}
      </div>


      <div>

        <span>
          {eyebrow}
        </span>

        <h2>
          {title}
        </h2>

        <p>
          {description}
        </p>

      </div>

    </div>

  );

}


/* =========================================================
   EMPTY STATE
========================================================= */

function EmptyState({
  text,
}) {

  return (

    <div className="empty-state">
      {text}
    </div>

  );

}


/* =========================================================
   PAPER CHAT
========================================================= */

function PaperChat({ file }) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submit = async (event) => {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading || !file) {
      return;
    }

    // Immediately show the user's question
    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: trimmedQuestion,
      },
    ]);

    // Clear input so the user can type the next question
    setQuestion("");
    setError("");
    setLoading(true);

    try {
      const data = await askPaper(
        file,
        trimmedQuestion
      );

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            data.answer ||
            "I couldn't find an answer in the paper.",
        },
      ]);
    } catch (err) {
      setError(
        err.message ||
          "Unable to answer your question."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="chat-section">

      {/* ================= CHAT HEADER ================= */}

      <div className="chat-header">

        <div className="wide-icon">
          <MessageSquare size={20} />
        </div>

        <div>
          <span>
            Paper assistant
          </span>

          <h2>
            Ask your research paper.
          </h2>

          <p>
            Explore the paper through natural language.
          </p>
        </div>

      </div>


      {/* ================= CHAT HISTORY ================= */}

      {messages.length > 0 && (

        <div className="chat-history">

          {messages.map(
            (message, index) => (

              <div
                key={index}
                className={`chat-message ${
                  message.role === "user"
                    ? "user-message"
                    : "assistant-message"
                }`}
              >

                <div className="message-label">

                  {message.role === "user" ? (
                    <>
                      <MessageSquare size={13} />
                      You
                    </>
                  ) : (
                    <>
                      <Sparkles size={13} />
                      ResearchWeaver
                    </>
                  )}

                </div>


                <p>
                  {message.content}
                </p>

              </div>

            )
          )}


          {/* Loading response */}

          {loading && (

            <div className="chat-message assistant-message">

              <div className="message-label">

                <Sparkles size={13} />

                ResearchWeaver

              </div>

              <div className="typing-indicator">

                <span />
                <span />
                <span />

              </div>

            </div>

          )}

        </div>

      )}


      {/* ================= ERROR ================= */}

      {error && (

        <div className="chat-error">

          <AlertTriangle size={16} />

          {error}

        </div>

      )}


      {/* ================= INPUT ================= */}

      <form
        className="chat-input"
        onSubmit={submit}
      >

        <MessageSquare size={18} />


        <input
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          placeholder="Ask anything about this paper..."
          disabled={loading}
        />


        <button
          type="submit"
          disabled={
            loading ||
            !question.trim() ||
            !file
          }
        >

          {loading ? (

            <Loader2
              size={18}
              className="spin"
            />

          ) : (

            <ArrowRight size={18} />

          )}

        </button>

      </form>

    </section>
  );
}

export {
  App,
  FeatureCard,
  LoadingScreen,
  ResearchDashboard,
  StatCard,
  SectionCard,
  ListSection,
  MetadataCard,
  KeywordsCard,
  AbstractCard,
  ResearchGaps,
  Difficulty,
  ExperimentPlanner,
  ExperimentBlock,
  ExperimentList,
  KnowledgeGraph,
  SectionHeader,
  EmptyState,
  PaperChat,
};

export default App;