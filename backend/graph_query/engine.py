import networkx as nx


class GraphEngine:

    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

        self.G = nx.Graph()

        # Add Nodes
        for node in nodes:
            self.G.add_node(
                node["id"],
                type=node.get("type", "Unknown"),
                data=node.get("data", {})
            )

        # Add Edges
        for edge in edges:
            self.G.add_edge(
                edge["source"],
                edge["target"],
                type=edge.get("type", "RELATED")
            )


    # -------------------------------
    # Query 0 — Get Customer Info
    # -------------------------------
    def get_customer_info(self, customer_id):

        customer_id = str(customer_id)

        for node in self.G.nodes:

            data = self.G.nodes[node]

            if data.get("type") == "Customer":

                customer_data = data.get("data", {})

                print(
                "Checking:",
                node,
                customer_data.get("customer"),
                customer_data.get("businessPartner")
            )

            if (
                customer_id in node
                or str(customer_data.get("customer")) in str(customer_id)
                or str(customer_data.get("businessPartner")) in str(customer_id)
            ):
                print("FOUND MATCH")
                return {
                    "id": node,
                    "type": "Customer",
                    "data": customer_data
                }

        return "Customer not found"


    # -------------------------------
    # Query 1 — Products With Most Billings
    # -------------------------------
    def products_with_most_billings(self):

        counts = {}

        for node in self.G.nodes:

            data = self.G.nodes[node]

            if data.get("type") == "Material":

                count = 0

                for neighbor in self.G.neighbors(node):

                    if self.G.nodes[neighbor].get("type") == "Invoice":
                        count += 1

                counts[node] = count

        sorted_counts = sorted(
            counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_counts[:10]


    # -------------------------------
    # Query 2 — Trace Billing Flow
    # -------------------------------
    def trace_billing_flow(self, billing_id):

        if billing_id not in self.G:
            return "Billing ID not found"

        visited = set()
        stack = [billing_id]

        flow = []

        while stack:

            node = stack.pop()

            if node in visited:
                continue

            visited.add(node)

            flow.append({
                "id": node,
                "type": self.G.nodes[node].get("type")
            })

            for neighbor in self.G.neighbors(node):
                stack.append(neighbor)

        return flow


    # -------------------------------
    # Query 3 — Find Broken Flows
    # -------------------------------
    def find_broken_flows(self):

        broken = []

        for node in self.G.nodes:

            data = self.G.nodes[node]

            if data.get("type") == "SalesOrder":

                neighbors = list(self.G.neighbors(node))

                has_delivery = any(
                    self.G.nodes[n].get("type") == "Delivery"
                    for n in neighbors
                )

                has_invoice = any(
                    self.G.nodes[n].get("type") == "Invoice"
                    for n in neighbors
                )

                if has_delivery and not has_invoice:
                    broken.append(node)

        return broken


    # -------------------------------
    # Query 4 — Get Full Graph
    # -------------------------------
    def get_full_graph(self):

        nodes = []
        edges = []

        for node in self.G.nodes:
            nodes.append({
                "id": node,
                "type": self.G.nodes[node].get("type"),
                "data": self.G.nodes[node].get("data")
            })

        for source, target in self.G.edges:
            edges.append({
                "source": source,
                "target": target,
                "type": self.G.edges[source, target].get("type")
            })

        return {
            "nodes": nodes,
            "edges": edges
        }