def build_graph(data):
    nodes = {}
    edges = []

    def add_node(node_id, node_type, data):
        if node_id not in nodes:
            nodes[node_id] = {
                "id": node_id,
                "type": node_type,
                "data": data
            }

    # -------------------
    # CUSTOMERS
    # -------------------
    for bp in data["business_partners"]:
        cid = f"Customer_{bp['businessPartner']}"
        add_node(cid, "Customer", bp)

    for addr in data["business_partner_address"]:
        cid = f"Customer_{addr['businessPartner']}"
        aid = f"Address_{addr['addressId']}"

        add_node(aid, "Address", addr)

        edges.append({
            "source": cid,
            "target": aid,
            "type": "HAS_ADDRESS"
        })

    # -------------------
    # SALES ORDERS
    # -------------------
    for so in data["sales_order_headers"]:
        so_id = f"SalesOrder_{so['salesOrder']}"
        cust_id = f"Customer_{so['soldToParty']}"

        add_node(so_id, "SalesOrder", so)

        edges.append({
            "source": cust_id,
            "target": so_id,
            "type": "PLACED_ORDER"
        })

    for item in data["sales_order_items"]:
        so_id = f"SalesOrder_{item['salesOrder']}"
        mat_id = f"Material_{item['material']}"

        add_node(mat_id, "Material", {"id": item["material"]})

        edges.append({
            "source": so_id,
            "target": mat_id,
            "type": "CONTAINS"
        })

    # -------------------
    # DELIVERY
    # -------------------
    for d in data["outbound_delivery_items"]:
        del_id = f"Delivery_{d['deliveryDocument']}"
        so_id = f"SalesOrder_{d['referenceSdDocument']}"

        add_node(del_id, "Delivery", d)

        edges.append({
            "source": so_id,
            "target": del_id,
            "type": "DELIVERED_AS"
        })

    # -------------------
    # BILLING
    # -------------------
    for b in data["billing_document_headers"]:
        inv_id = f"Invoice_{b['billingDocument']}"
        cust_id = f"Customer_{b['soldToParty']}"
        acc_id = f"Accounting_{b['accountingDocument']}"

        add_node(inv_id, "Invoice", b)
        add_node(acc_id, "Accounting", {"id": b["accountingDocument"]})

        edges.append({"source": inv_id, "target": cust_id, "type": "BILLED_TO"})
        edges.append({"source": inv_id, "target": acc_id, "type": "POSTED_TO"})

    for item in data["billing_document_items"]:
        inv_id = f"Invoice_{item['billingDocument']}"
        so_id = f"SalesOrder_{item['referenceSdDocument']}"
        mat_id = f"Material_{item['material']}"

        add_node(mat_id, "Material", {"id": item["material"]})

        edges.append({"source": inv_id, "target": so_id, "type": "FROM_ORDER"})
        edges.append({"source": inv_id, "target": mat_id, "type": "HAS_ITEM"})

    for c in data["billing_document_cancellation"]:
        if c["billingDocumentIsCancelled"]:
            inv_id = f"Invoice_{c['billingDocument']}"
            cancel_id = f"Cancel_{c['billingDocument']}"

            add_node(cancel_id, "Cancellation", c)

            edges.append({
                "source": inv_id,
                "target": cancel_id,
                "type": "CANCELLED"
            })

    # -------------------
    # JOURNAL ENTRY
    # -------------------
    for j in data["journal_entry_items_accounts_receivable"]:
        acc_id = f"Accounting_{j['accountingDocument']}"
        inv_id = f"Invoice_{j['referenceDocument']}"
        cust_id = f"Customer_{j['customer']}"

        add_node(acc_id, "Accounting", j)

        edges.append({"source": acc_id, "target": inv_id, "type": "REFERS_TO"})
        edges.append({"source": acc_id, "target": cust_id, "type": "FOR_CUSTOMER"})

    # -------------------
    # PAYMENTS
    # -------------------
    for p in data["payments_accounts_receivable"]:
        pay_id = f"Payment_{p['accountingDocument']}"
        cust_id = f"Customer_{p['customer']}"
        acc_id = f"Accounting_{p['accountingDocument']}"

        add_node(pay_id, "Payment", p)

        edges.append({"source": pay_id, "target": cust_id, "type": "PAID_BY"})
        edges.append({"source": pay_id, "target": acc_id, "type": "SETTLES"})

    return list(nodes.values()), edges