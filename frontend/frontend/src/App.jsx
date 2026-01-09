import { useState } from "react";

function App() {
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:7860/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setAudioUrl(data.audioUrl);
    setLoading(false);
  }

  return (
    <div style={{ padding: 40 }}>
      <h2>📄 PDF Audio Reader</h2>

      <input type="file" accept="application/pdf" onChange={handleUpload} />

      {loading && <p>Processing PDF...</p>}

      {audioUrl && (
        <div>
          <h3>🎧 Audio Output</h3>
          <audio controls src={audioUrl} />
        </div>
      )}
    </div>
  );
}

export default App;
