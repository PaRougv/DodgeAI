import networkx as nx

class GraphEngine:

    def __init__(self, nodes, edges):
        self.G = nx.Graph()

        for node in nodes:
            self.G.add_node(node["id"], **node)

        for edge in edges:
            self.G.add_edge(edge["source"], edge["target"], **edge)
        
    

    def get_customer_info(self, customer_id):

        for node in self.nodes:
            if node["type"] == "Customer":
                if customer_id in node["id"] or customer_id in str(node["data"]):
                    return node

        return "Customer not found"


    # Query 1
    def products_with_most_billings(self):

        counts = {}

        for node in self.G.nodes:

            data = self.G.nodes[node]

            if data["type"] == "Material":

                count = 0

                for neighbor in self.G.neighbors(node):

                    if self.G.nodes[neighbor]["type"] == "Invoice":
                        count += 1

                counts[node] = count

        sorted_counts = sorted(
            counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_counts[:10]


    # Query 2
    def trace_billing_flow(self, billing_id):

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
                "type": self.G.nodes[node]["type"]
            })

            for neighbor in self.G.neighbors(node):
                stack.append(neighbor)

        return flow


    # Query 3
    def find_broken_flows(self):

        broken = []

        for node in self.G.nodes:

            data = self.G.nodes[node]

            if data["type"] == "SalesOrder":

                neighbors = list(self.G.neighbors(node))

                has_delivery = any(
                    self.G.nodes[n]["type"] == "Delivery"
                    for n in neighbors
                )

                has_invoice = any(
                    self.G.nodes[n]["type"] == "Invoice"
                    for n in neighbors
                )

                if has_delivery and not has_invoice:
                    broken.append(node)

        return broken