from flask import Flask, render_template, request, jsonify

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

from config import API_KEY, PROJECT_ID, URL

app = Flask(__name__)

credentials = Credentials(
    url=URL,
    api_key=API_KEY
)

model = ModelInference(
    model_id="ibm/granite-4-h-small",
    credentials=credentials,
    project_id=PROJECT_ID
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()

    startup_idea = data["idea"]

    prompt = f"""
You are an expert Startup Blueprint Generator and Business Consultant.

Your task is to transform the user's startup idea into a professional startup blueprint using ONLY the provided reference context.

Startup Idea:
{startup_idea}

Generate a practical startup blueprint of approximately **500–900 words**. Include only the sections that are relevant to the startup idea. If a section is not applicable (for example, Technology Stack for a non-technical business or Government Schemes if none are relevant in the provided context), omit that section instead of forcing content.

Generate the blueprint using the following sections wherever appropriate:

1. Executive Summary
   - Brief overview of the startup idea.(3-4 lines)

2. Problem Statement(5-6 bullet points)
   - What problem is being solved?
   - Why is it important?

3. Market Opportunity(4-5 sentence  points)
   - Target audience
   - Market need
   - Market gap

4. Existing Solutions & Limitations()
   - Current competitors or existing solutions.
   - Their shortcomings.

5. Proposed Solution (step by step)
   - Explain how the startup solves the problem.
   - Highlight the major features or services.

6. Unique Value Proposition (USP)(4 lines)
   - Explain what makes the startup unique.
   - Highlight its competitive advantage.

7. Business Model
   Include a concise Business Model Canvas where appropriate:
   - Key Partners
   - Key Activities
   - Key Resources
   - Value Proposition
   - Customer Relationships
   - Channels
   - Customer Segments
   - Cost Structure
   - Revenue Streams

8. Revenue Model
   - Explain how the startup generates revenue.(donot over hype the amount of revenue)

9. Technology Stack (Only if applicable)
   - Suggest suitable technologies, AI tools, cloud services, APIs, databases, or deployment platforms only if applicable donot force it.

10. Estimated Budget( give relevant proofs)
   - Provide an approximate cost breakdown.
   - Include an estimated total cost.

11. Go-to-Market Strategy
   - Target customers
   - Positioning
   - Distribution channels
   - Pricing strategy
   - Early success metrics

12. Competitor Analysis (If applicable)
   - Compare with existing competitors.
   - Explain competitive advantages.

13. SWOT Analysis (If useful)
   - Strengths
   - Weaknesses
   - Opportunities
   - Threats

14. Risks & Challenges
   - Technical
   - Financial
   - Operational
   - Legal
   - Market

15. Relevant Government Schemes(true ones needed, donot invent yourself )
   - Recommend ONLY schemes available in the reference context.

16. Potential Funding Sources
   - Recommend suitable funding sources only when appropriate.

17. Implementation Roadmap
   - High-level roadmap from idea validation to launch.

18. Expected Impact
   - Business
   - Customer
   - Social
   - Economic
   - Environmental (if applicable)

19. Conclusion(4-5 bullet points)
   - Summarize why the startup has potential.
   - Recommend the next logical steps.

REFERENCE CONTEXT


1. Startup India Seed Fund Scheme (SISFS)

A Government of India scheme run by DPIIT.

Eligible startups must:
- Be DPIIT-recognised.
- Be incorporated for less than 2 years.
- Have at least 51% Indian promoter shareholding.
- Must not have received more than ₹10 lakh from other government schemes.

Funding:
- Up to ₹20 lakh as a milestone-based grant for proof-of-concept and prototyping.
- Up to ₹50 lakh through convertible debentures or debt instruments for market entry and scaling.
- Funds are disbursed through approved incubators.

--------------------------------------------------

2. Business Model Canvas

- Key Partners
- Key Activities
- Key Resources
- Value Proposition
- Customer Relationships
- Channels
- Customer Segments
- Cost Structure
- Revenue Streams

--------------------------------------------------

3. Go-to-Market Framework

- Define target customers.
- Craft positioning and messaging.
- Select distribution channels.
- Define pricing strategy.
- Define early success metrics:
  - Customer Acquisition Cost (CAC)
  - Activation Rate
  - Retention Rate

--------------------------------------------------

4. Common Early-Stage Funding Sources in India

- Startup India Seed Fund Scheme (SISFS)
- Angel Investors
- Venture Capital
- Incubators
- Accelerators
- MSME Schemes
- State Government Startup Schemes 


Formatting Guidelines:
- Use clear section headings.
- Use concise bullet points wherever appropriate.
- Keep explanations practical, realistic, and business-oriented.
- Include only sections that are relevant to the startup idea.
- Do NOT invent facts, statistics, government schemes, funding programs, or market data.
- If any information is unavailable in the reference context, clearly mention that instead of making assumptions.
- Return ONLY the startup blueprint.
- Do not repeat the prompt, instructions, or reference context.
-You must answer ONLY queries related to startup blueprint generation and the provided reference context.
-If the user asks anything unrelated to startup planning, entrepreneurship, business strategy, funding, market analysis, business models, or the provided reference context, politely decline by responding with exactly three sentences:

"I am sorry, but I cannot assist with that request. I am specifically designed to generate startup blueprints and provide entrepreneurship-related guidance based on my reference context. Please ask a startup-related question or provide a startup idea to receive a business blueprint."
-Never answer unrelated questions, even if you know the answer.
-Do not add invented facts, statistics, competitors, market information, customer details, or assumptions that are not explicitly available in the reference context.


"""
    params = {
    "decoding_method": "greedy",
    "max_new_tokens": 1400,
    "min_new_tokens": 400,
    "temperature": 0.2,
    "repetition_penalty": 1.05
}
    
    response = model.generate_text(
    prompt=prompt,
    params=params
)

    return jsonify({
        "result": response
    })


if __name__ == "__main__":
    app.run(debug=True)