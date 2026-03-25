import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def interpret_query(query: str):
    print("Accha Lawde")
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

User Query:
{query}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        plan = response.choices[0].message.content.strip().lower()

        print("LLM PLAN:", plan)

        if "products_with_most_billings" in plan:
            return "products_with_most_billings"

        if "trace_billing_flow" in plan:
            return "trace_billing_flow"

        if "find_broken_flows" in plan:
            return "find_broken_flows"

        if "customer" in plan or "get_customer_info" in plan:
            return "get_customer_info"

        return "unknown"

    except Exception as e:
        print("Groq Error:", e)
        return "unknown"