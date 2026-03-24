import google.generativeai as genai
import os

# Configure Gemini
genai.configure(
    api_key="AIzaSyDInwKZuM-NMMgjc12yiZxUiTBTDIhhw5Q"
)

# Use latest stable model
model = genai.GenerativeModel("gemini-1.5-flash-latest")


def interpret_query(query: str):

    prompt = f"""
You are a graph query planner.

Convert the user query into ONE of the following functions:

products_with_most_billings
trace_billing_flow
find_broken_flows
get_customer_info

Rules:
- Return ONLY function name
- No explanation
- No extra text
- If user asks about customer, return get_customer_info

User Query:
{query}
"""

    try:
        response = model.generate_content(prompt)

        print("LLM RAW RESPONSE:", response.text)

        if not response or not response.text:
            return "unknown"

        plan = response.text.strip().lower()

        # Debug (optional but useful)
        print("LLM PLAN:", plan)

        # Safety cleanup
        if "products_with_most_billings" in plan:
            return "products_with_most_billings"

        if "trace_billing_flow" in plan:
            return "trace_billing_flow"

        if "find_broken_flows" in plan:
            return "find_broken_flows"

        if "customer" in plan or "get_customer_info" in plan:
            return "get_customer_info"

        # fallback heuristic
        if "customer" in query.lower():
            return "get_customer_info"

        return "unknown"

    except Exception as e:
        print("Gemini Error:", e)
        return "unknown"