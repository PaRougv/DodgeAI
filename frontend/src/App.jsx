import React, { useEffect, useState, useMemo } from "react";
import ReactFlow, { Background, Controls } from "reactflow";
import "reactflow/dist/style.css";
import axios from "axios";

function getColor(type) {
  const colors = {
    Customer: "#ff6b6b",
    SalesOrder: "#4dabf7",
    Delivery: "#ffd43b",
    Invoice: "#69db7c",
    Payment: "#845ef7",
    Accounting: "#f06595",
    Material: "#ffa94d",
    Cancellation: "#adb5bd",
  };
  return colors[type] || "#999";
}

// 🔥 Find most connected node (hub)
function findHub(nodes, edges) {
  const degree = {};
  edges.forEach((e) => {
    degree[e.source] = (degree[e.source] || 0) + 1;
    degree[e.target] = (degree[e.target] || 0) + 1;
  });

  return nodes.reduce((best, n) => {
    return (degree[n.id] || 0) > (degree[best.id] || 0)
      ? n
      : best;
  }, nodes[0]).id;
}

// 🔥 PERFECT NON-OVERLAPPING LAYOUT
function layoutByGroups(nodes, edges) {
  const groups = {};

  nodes.forEach((n) => {
    if (!groups[n.type]) groups[n.type] = [];
    groups[n.type].push(n);
  });

  const types = Object.keys(groups);

  const centerX = 800;
  const centerY = 500;

  const clusterCircleRadius = 450;
  const angleStep = (2 * Math.PI) / types.length;

  const result = [];

  types.forEach((group, idx) => {
    const groupNodes = groups[group];

    const angle = idx * angleStep;

    const clusterX = centerX + clusterCircleRadius * Math.cos(angle);
    const clusterY = centerY + clusterCircleRadius * Math.sin(angle);

    const hub = findHub(groupNodes, edges);

    const baseRadius = 80 + groupNodes.length * 0.3;

    groupNodes.forEach((node, i) => {
      if (node.id === hub) {
        result.push({ ...node, x: clusterX, y: clusterY });
      } else {
        const layer = Math.floor(i / 40);
        const layerRadius = baseRadius + layer * 30;

        const angle = ((i % 40) / 40) * 2 * Math.PI;

        result.push({
          ...node,
          x: clusterX + layerRadius * Math.cos(angle),
          y: clusterY + layerRadius * Math.sin(angle),
        });
      }
    });
  });

  return result;
}

function App() {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [hovered, setHovered] = useState(null);
  const [locked, setLocked] = useState(null);
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")

  useEffect(() => {
    axios.get("http://localhost:8000/graph").then((res) => {
      const rawNodes = res.data.nodes.map((n) => ({
        id: n.id,
        type: n.type,
        data: n,
      }));

      const rawEdges = res.data.edges.map((e, i) => ({
        id: i.toString(),
        source: e.source,
        target: e.target,
      }));

      const positioned = layoutByGroups(rawNodes, rawEdges);

      const rfNodes = positioned.map((n) => ({
        id: n.id,
        position: { x: n.x, y: n.y },
        data: n,
        style: {
          width: 4,
          height: 4,
          borderRadius: "50%",
          background: getColor(n.type),
        },
      }));

      const rfEdges = rawEdges.map((e) => ({
        id: e.id,
        source: e.source,
        target: e.target,
        style: {
          stroke: "#6ba3ff",
          strokeWidth: 1,
          opacity: 0.25,
        },
      }));

      setNodes(rfNodes);
      setEdges(rfEdges);
    });
  }, []);

  const sendQuery = async () => {

    if (!input.trim()) return;

    const res = await axios.post(
      "http://localhost:8000/query",
      {
        query: input
      }
    )

    setMessages(prev => [
      ...prev,
      { role: "user", text: input },
      { role: "assistant", text: JSON.stringify(res.data.answer, null, 2) }
    ])

    setInput("")
  }

  const activeNode = locked || hovered;

  const nodeTypes = useMemo(() => ({}), []);

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        onNodeMouseEnter={(e, node) => {
          if (!locked) setHovered(node);
        }}
        onNodeMouseLeave={() => {
          if (!locked) setHovered(null);
        }}
        onNodeClick={(e, node) => {
          if (locked?.id === node.id) {
            setLocked(null);
          } else {
            setLocked(node);
          }
        }}
      >
        <Background gap={12} size={1} />
        <Controls />
      </ReactFlow>

{/* Chat UI */}
<div
  style={{
    position: "absolute",
    bottom: 20,
    left: 20,
    width: "350px",
    height: "400px",
    background: "#111",
    color: "white",
    borderRadius: "10px",
    display: "flex",
    flexDirection: "column",
    overflow: "hidden",
    zIndex: 10
  }}
>
  <div
    style={{
      flex: 1,
      padding: "10px",
      overflowY: "auto",
      fontSize: "12px"
    }}
  >
    {messages.map((m, i) => (
      <div
        key={i}
        style={{
          marginBottom: "8px",
          padding: "6px",
          background:
            m.role === "user" ? "#1a73e8" : "#222",
          borderRadius: "5px"
        }}
      >
        <b>{m.role}</b>
        <div>{m.text}</div>
      </div>
    ))}
  </div>

  <div
    style={{
      display: "flex",
      borderTop: "1px solid #333"
    }}
  >
    <input
      value={input}
      onChange={(e)=>setInput(e.target.value)}
      placeholder="Ask graph..."
      style={{
        flex: 1,
        padding: "8px",
        background: "#111",
        color: "white",
        border: "none"
      }}
    />

    <button
      onClick={sendQuery}
      style={{
        padding: "8px 12px",
        background: "#1a73e8",
        border: "none",
        color: "white"
      }}
    >
      Send
    </button>
  </div>

</div>

      {activeNode && (
        <div
          style={{
            position: "absolute",
            right: 20,
            top: 20,
            background: "#111",
            color: "white",
            padding: "10px",
            borderRadius: "8px",
            width: "300px",
            maxHeight: "400px",
            overflow: "auto",
            fontSize: "10px",
          }}
        >
          <h4>
            {activeNode.data.type}
            {locked && " (Locked)"}
          </h4>
          <pre>
            {JSON.stringify(activeNode.data.data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;