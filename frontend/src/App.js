import React from "react";
import ChatBox from "./components/ChatBox";
import "./styles.css";

function App() {
  return (
    <div className="app">
      <div className="sidebar">
        <h2>AI CRM</h2>

        <div className="quick">
          <button onClick={() => window.send("Show all interactions")}>
            Fetch
          </button>
        </div>

        <div className="quick">
          <button onClick={() => window.send("Summarize this HCP")}>
            Summary
          </button>
        </div>

        <div className="quick">
          <button onClick={() => window.send("Doctor not interested")}>
            Suggest
          </button>
        </div>
      </div>

      <ChatBox />
    </div>
  );
}

export default App;