from fastapi import FastAPI
from graph_builder.builder import build_graph
from data_loader.parser import load_jsonl
from fastapi.middleware.cors import CORSMiddleware

# NEW IMPORTS
from graph_query.engine import GraphEngine
from llm.interpreter import interpret_query
from llm.guardrails import validate

import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GLOBAL GRAPH ENGINE
graph_engine = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data", "sap-o2c-data")

print("DATA DIR:", DATA_DIR)


@app.get("/graph")
def get_graph():

    global graph_engine

    data = {
        "business_partners": load_jsonl(
            os.path.join(DATA_DIR, "business_partners", "part-20251119-133435-168.jsonl")
        ),

        "business_partner_address": load_jsonl(
            os.path.join(DATA_DIR, "business_partner_addresses", "part-20251119-133436-580.jsonl")
        ),

        "sales_order_headers": load_jsonl(
            os.path.join(DATA_DIR, "sales_order_headers", "part-20251119-133429-440.jsonl")
        ),

        "sales_order_items": load_jsonl(
            os.path.join(DATA_DIR, "sales_order_items", "part-20251119-133429-452.jsonl")
        ),

        "outbound_delivery_items": load_jsonl(
            os.path.join(DATA_DIR, "outbound_delivery_items", "part-20251119-133431-439.jsonl")
        ),

        "billing_document_headers": load_jsonl(
            os.path.join(DATA_DIR, "billing_document_headers", "part-20251119-133433-228.jsonl")
        ),

        "billing_document_items": load_jsonl(
            os.path.join(DATA_DIR, "billing_document_items", "part-20251119-133432-233.jsonl")
        ),

        "billing_document_cancellation": load_jsonl(
            os.path.join(DATA_DIR, "billing_document_cancellations", "part-20251119-133433-51.jsonl")
        ),

        "journal_entry_items_accounts_receivable": load_jsonl(
            os.path.join(DATA_DIR, "journal_entry_items_accounts_receivable", "part-20251119-133433-74.jsonl")
        ),

        "payments_accounts_receivable": load_jsonl(
            os.path.join(DATA_DIR, "payments_accounts_receivable", "part-20251119-133434-100.jsonl")
        ),
    }

    nodes, edges = build_graph(data)

    # BUILD GRAPH ENGINE
    graph_engine = GraphEngine(nodes, edges)

    return {"nodes": nodes, "edges": edges}


@app.post("/query")
def query(body: dict):

    print("Entered over here")

    global graph_engine

    # GRAPH NOT INITIALIZED
    if graph_engine is None:
        return {
            "answer": "Graph not initialized. Call /graph first."
        }

    query = body["query"]

    # Guardrails
    if not validate(query):
        return {
            "answer": "This system is designed to answer dataset related queries only."
        }

    # INTERPRET QUERY
    plan = interpret_query(query).lower().strip()

    if "products_with_most_billings" in plan:
        result = graph_engine.products_with_most_billings()

    elif "trace_billing_flow" in plan:
        billing_id = body.get("billing_id")
        result = graph_engine.trace_billing_flow(billing_id)

    elif "find_broken_flows" in plan:
        result = graph_engine.find_broken_flows()

    elif "get_customer_info" in plan:
        customer_id = body.get("customer_id") or query
        result = graph_engine.get_customer_info(customer_id)

    else:
        result = "Query not supported"

    return {
        "answer": result
    }