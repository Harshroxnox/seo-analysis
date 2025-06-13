import { useState } from 'react'
import axios from 'axios';
import './App.css'

function App() {
  const [text, setText] = useState('');
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    if (!text.trim()) return;

    try {
      setError(null);
      const res = await axios.post('http://localhost:5000/api/metrics', { text });
      setMetrics(res.data);
    } catch (err) {
      console.log(err)
      setError('Failed to analyze text.');
    }
  };

  return (
    <div className='app'>
      <h1>SEO Analyzer App</h1>

      <div className='input'>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text to analyze..."
          rows={10}
          cols={60}
        />
        <br />
        <button onClick={handleSubmit}>Analyze</button>
      </div>


      {error && <p style={{ color: 'red' }}>{error}</p>}

      <h1 className='result-heading'>Results</h1>
        <div className='results'>
          {metrics && (
            <div className="metrics">
              <h2>Metrics</h2>
              <ul>
                <li key={"ari"}><strong>{"Automated Readability Index"}:</strong> {metrics.ari.toFixed(2)}</li>
                <li key={"coleman_liau"}><strong>{"Coleman Liau Index"}:</strong> {metrics.coleman_liau.toFixed(2)}</li>
                <li key={"dale_chall"}><strong>{"Dale Chall Readability Formula"}:</strong> {metrics.dale_chall.toFixed(2)}</li>
                <li key={"flesch"}><strong>{"Flesch Reading Ease"}:</strong> {metrics.flesch.toFixed(2)}</li>
                <li key={"flesch_kincaid"}><strong>{"Flesch Kincaid Grade Level"}:</strong> {metrics.flesch_kincaid.toFixed(2)}</li>
                <li key={"gunning_fog"}><strong>{"Gunning Fog Index"}:</strong> {metrics.gunning_fog.toFixed(2)}</li>
                <li key={"linsear_write"}><strong>{"Linsear Write Formula"}:</strong> {metrics.linsear_write.toFixed(2)}</li>
                <li key={"spache"}><strong>{"Spache Readability Formula"}:</strong> {metrics.spache.toFixed(2)}</li>
              </ul>
            </div>
          )}
        </div>
    </div>
  )
}

export default App
