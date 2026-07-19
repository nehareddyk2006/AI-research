import json
import os

from dotenv import load_dotenv
from google import genai

from src.ai.prompts import PAPER_ANALYSIS_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.1-flash-lite"
)


def analyze_paper(text: str) -> dict:
    """
    Analyze a research paper using a single Gemini call.

    Returns:
    {
        summary,
        research_problem,
        methodology,
        datasets,
        models,
        evaluation_metrics,
        keywords,
        limitations,
        future_work,
        knowledge_graph
    }
    """

    prompt = PAPER_ANALYSIS_PROMPT + text[:30000]

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    output = response.text.strip()

    # Remove markdown fences if Gemini adds them
    if output.startswith("```"):
        output = (
            output
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:
        data = json.loads(output)

    except json.JSONDecodeError:
        raise Exception(
            f"Gemini returned invalid JSON:\n\n{output}"
        )

    # -------- Default values -------- #

    data.setdefault("summary", "")
    data.setdefault("research_problem", "")
    data.setdefault("methodology", "")

    data.setdefault("datasets", [])
    data.setdefault("models", [])
    data.setdefault("evaluation_metrics", [])
    data.setdefault("keywords", [])
    data.setdefault("limitations", [])
    data.setdefault("future_work", [])

    data.setdefault(
        "knowledge_graph",
        {
            "nodes": [],
            "edges": []
        }
    )
    data.setdefault("research_gaps", [])
    data.setdefault(
        "experiment_plan",
        {
            "objective": "",
            "dataset": "",
            "preprocessing": [],
            "baseline_models": [],
            "proposed_model": "",
            "evaluation_metrics": [],
            "expected_results": ""
        }
    )

    return data