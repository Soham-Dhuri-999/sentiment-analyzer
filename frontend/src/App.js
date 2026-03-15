import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeText = async () => {
    if (!text) return;
    setLoading(true);
    setResult(null);

    try {
      await fetch("https://sentiment-analyzer-backend-9uys.onrender.com/");
      await new Promise((resolve) => setTimeout(resolve, 2000));

      const response = await fetch("https://sentiment-analyzer-backend-9uys.onrender.com/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();

      if (data.error) {
        setResult({ label: "ERROR", score: 0, error: data.error });
      } else {
        setResult(data);
      }

    } catch (err) {
      setResult({ label: "ERROR", score: 0, error: "Could not reach server." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "60px auto", fontFamily: "sans-serif", padding: "0 20px" }}>
      <h1>Sentiment Analyzer</h1>
      <p>Enter any sentence and the AI will analyze its sentiment.</p>
      <textarea
        rows={4}
        style={{ width: "100%", padding: "12px", fontSize: "16px", marginBottom: "12px" }}
        placeholder="Type something here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button
        onClick={analyzeText}
        disabled={loading}
        style={{ padding: "10px 24px", fontSize: "16px", cursor: "pointer" }}
      >
        {loading ? "Waking up AI... please wait (~15s)" : "Analyze"}
      </button>

      {result && (
        <div style={{
          marginTop: "24px",
          padding: "20px",
          background: result.label === "POSITIVE" ? "#d4edda" : result.label === "ERROR" ? "#fff3cd" : "#f8d7da",
          borderRadius: "8px"
        }}>
          {result.label === "ERROR" ? (
            <p style={{ color: "#856404" }}>⚠️ Error: {result.error}</p>
          ) : (
            <>
              <h2>{result.label}</h2>
              <p>Confidence: {result.score}%</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;