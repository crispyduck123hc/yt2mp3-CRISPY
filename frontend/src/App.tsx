import { useState } from 'react';

function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('');

  const handleDownload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url) return;

    setLoading(true);
    setStatus('Processing your download...');

    try {
      // Because of your Vite Proxy, we call /api/download
      const title_response = await fetch('/api/title', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: url })
      });
        const title = await title_response.json()

      const file_response = await fetch('/api/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url }),
      });

      if (!file_response.ok) {
        const errorData = await file_response.json();
        throw new Error(errorData.detail || 'Download failed');
      }

      // Handle the binary data (the MP3 file)
      const blob = await file_response.blob();

      // Create a temporary reference to blob
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      // Add download attribute to anchor
      // Try to get filename from header or fallback
      link.setAttribute('download', `${title}.mp3`);
      // automatic download of file
      document.body.appendChild(link);
      link.click();

      // Cleanup
      link.parentNode?.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);

      setStatus('Success! Check your downloads folder.');
    } catch (err: any) {
      setStatus(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '50px auto', padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>🎵 YouTube MP3 Downloader</h1>
      <p>Enter a YouTube URL to extract the audio.</p>

      <form onSubmit={handleDownload} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <input
          type="url"
          placeholder="https://www.youtube.com/watch?v=..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
          style={{ padding: '12px', borderRadius: '4px', border: '1px solid #ccc' }}
        />

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: '12px',
            backgroundColor: loading ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Downloading...' : 'Get MP3'}
        </button>
      </form>

      {status && (
        <div style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
          {status}
        </div>
      )}
    </div>
  );
}

export default App;