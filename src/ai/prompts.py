PAPER_ANALYSIS_PROMPT = """
You are an expert AI research paper analyst.

Analyze the following research paper and return ONLY valid JSON.

The JSON must have EXACTLY this structure:

{
    "summary": "",
    "research_problem": "",
    "methodology": "",
    "datasets": [],
    "models": [],
    "evaluation_metrics": [],
    "keywords": [],
    "limitations": [],
    "future_work": [],

    "knowledge_graph": {
        "nodes": [
            {
                "id": "",
                "type": "",
                "color": ""
            }
        ],

        "edges": [
            {
                "source": "",
                "target": "",
                "relation": ""
            }
        ]
    },
    "research_gaps":[
    {
        "title":"",
        "description":"",
        "reason":"",
        "future_direction":"",
        "difficulty":"Easy"
    }
],
"experiment_plan": {
    "objective": "",
    "dataset": "",
    "preprocessing": [],
    "baseline_models": [],
    "proposed_model": "",
    "evaluation_metrics": [],
    "expected_results": ""
}
}

Knowledge Graph Rules:

- Extract ONLY the most important concepts.
- Maximum 20 nodes.
- Maximum 30 edges.
- No duplicate nodes.
- Keep node names short (1-3 words).
- Every edge MUST contain a meaningful relationship.
Research Gap Rules:

- Identify 3 to 5 meaningful research gaps.
- Base the gaps on the paper's limitations, future work, methodology, datasets, or unexplored areas.
- Do not invent unsupported claims.
- Each gap must include:
    - title
    - description
    - reason
    - future_direction
    - difficulty (Easy, Medium, or Hard)
Experiment Planner Rules:

Based on the paper, generate a realistic experiment plan.

Include:

- objective
- recommended dataset
- preprocessing steps
- baseline models
- one proposed improved model
- evaluation metrics
- expected results

The plan should be practical, technically sound, and directly related to the uploaded paper.

Do not invent unrealistic datasets or methods.

Allowed node types:

- Model
- Method
- Dataset
- Metric
- Concept
- Domain
- Task
- Problem
- Technique
- Application

Use ONLY these colors:

Model        -> "#6366F1"
Method       -> "#10B981"
Dataset      -> "#F59E0B"
Metric       -> "#EF4444"
Concept      -> "#8B5CF6"
Domain       -> "#06B6D4"
Task         -> "#EC4899"
Problem      -> "#DC2626"
Technique    -> "#14B8A6"
Application  -> "#F97316"

Example:

{
    "id":"Transformer",
    "type":"Model",
    "color":"#6366F1"
}

Example Edge:

{
    "source":"Transformer",
    "target":"Attention",
    "relation":"uses"
}

Rules:

- Do NOT include markdown.
- Do NOT include explanations.
- Do NOT wrap the JSON inside ```json.
- Return ONLY the JSON object.
- If any field is unavailable, return an empty string or an empty list.

Research Paper:

"""