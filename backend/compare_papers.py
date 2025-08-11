def compare_papers(paper1, paper2):
    prompt = f"""
    Compare these two research papers and present results in a table:
    
    Paper 1: {paper1}
    Paper 2: {paper2}
    
    Compare based on:
    - Research Problem
    - Methodology
    - Dataset Used
    - Results & Metrics
    - Limitations
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    
    # Extract the content properly for structured output
    return response.candidates[0].content.parts[0].text
