const API_BASE_URL = "https://ai-research-apg6.onrender.com";
export async function analyzePaper(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/analyze`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    let message = "Unable to analyze the paper.";

    try {
      const error = await response.json();
      message = error.detail || message;
    } catch {
      // Keep default error
    }

    throw new Error(message);
  }

  return response.json();
}


export async function askPaper(file, question) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_BASE_URL}/chat?question=${encodeURIComponent(question)}`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    let message = "Unable to answer the question.";

    try {
      const error = await response.json();
      message = error.detail || message;
    } catch {
      // Keep default error
    }

    throw new Error(message);
  }

  return response.json();
}