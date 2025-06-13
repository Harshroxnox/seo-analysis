import { useState } from 'react'
import axios from 'axios';
import './App.css'

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(false)
  const [metrics, setMetrics] = useState(null);
  const [density, setDensity] = useState(null);
  const [keywords, setKeywords] = useState([]);
  const [selected, setSelected] = useState([]);
  const [coarseTopics, setCoarseTopics] = useState([]);
  const [topics, setTopics] = useState([]);
  const [entities, setEntities] = useState([]);
  const [error, setError] = useState(null);

  const convertToArray = (input) => {
    return input
      .split(',')
      .map(word => word.trim())
      .filter(word => word);
  }

  const toggleKeyword = (e) => {
    const keyword = e.target.value;
    if(selected.includes(keyword)){
      // remove the keyword
      setSelected(selected.filter(k => k != keyword));
    }else {
      // add the keyword
      setSelected([...selected, keyword]);
    }
  }

  const handleInsertKeyword = async () => {
    console.log(selected);
  }

  const handleAnalyze = async () => {
    if (!text.trim()) return;

    try {
      setError(null);
      setResult(true);

      const metrics_res = await axios.post('http://localhost:5000/api/metrics', { text });
      const density_res = await axios.post('http://localhost:5000/api/word_density', { text });
      const keyword_res = await axios.post('http://localhost:5000/api/keywords', { text });
      const analyze_res = await axios.post('http://localhost:5000/api/analyze', { text });
      
      setDensity(density_res.data);
      setMetrics(metrics_res.data);
      setKeywords(convertToArray(keyword_res.data.keywords));

      setCoarseTopics(analyze_res.data.coarseTopics);
      setTopics(analyze_res.data.topics);
      setEntities(analyze_res.data.entities);

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
        <button onClick={handleAnalyze}>Analyze</button>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {result && <h1 className='result-heading'>Results</h1>}
      <div className='results'>

        {metrics && (
          <div className="two-col sub-results">
            <h2>Metrics</h2>
            <hr></hr>
            <ul>
              <li key={"ari"}><strong>{"Automated Readability Index"}:</strong> <span>{metrics.ari.toFixed(2)}</span></li>
              <li key={"coleman_liau"}><strong>{"Coleman Liau Index"}:</strong> <span>{metrics.coleman_liau.toFixed(2)}</span></li>
              <li key={"dale_chall"}><strong>{"Dale Chall Readability Formula"}:</strong> <span>{metrics.dale_chall.toFixed(2)}</span></li>
              <li key={"flesch"}><strong>{"Flesch Reading Ease"}:</strong> <span>{metrics.flesch.toFixed(2)}</span></li>
              <li key={"flesch_kincaid"}><strong>{"Flesch Kincaid Grade Level"}:</strong> <span>{metrics.flesch_kincaid.toFixed(2)}</span></li>
              <li key={"gunning_fog"}><strong>{"Gunning Fog Index"}:</strong> <span>{metrics.gunning_fog.toFixed(2)}</span></li>
              <li key={"linsear_write"}><strong>{"Linsear Write Formula"}:</strong> <span>{metrics.linsear_write.toFixed(2)}</span></li>
              <li key={"spache"}><strong>{"Spache Readability Formula"}:</strong> <span>{metrics.spache.toFixed(2)}</span></li>
            </ul>
          </div>
        )}

        {density && (
          <div className="two-col sub-results">
            <h2>Word Density</h2>
            <hr></hr>
            <ul>
              {Object.entries(density).map(([key, value]) => (
                <li key={key}><strong>{key}:</strong> <span>{value}%</span></li>
              ))}
            </ul>
          </div>
        )}

        {keywords.length!=0 && (
          <div className="single-col sub-results">
            <h2>Keywords</h2>
            <hr></hr>
            <ul>
              {keywords.map((value, index) => (
                <li key={index}>{value}</li>
              ))}
            </ul>
          </div>
        )}

      </div>

      {coarseTopics.length!=0 && (
        <div className="table-container">
          <h2>Coarse Topics</h2>
          <table className="coarse-table">
            <thead>
              <tr>
                <th>Label</th>
                <th>Score</th>
                <th>Wiki Link</th>
              </tr>
            </thead>
            <tbody>
              {coarseTopics.map((topic) => (
                <tr key={topic.id}>
                  <td>{topic.label}</td>
                  <td>{topic.score.toFixed(2)}</td>
                  <td>
                    <a href={topic.wikiLink} target="_blank" rel="noopener noreferrer">
                      {topic.wikiLink}
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {topics.length!=0 && (
        <div className="table-container">
          <h2>Topics</h2>
          <table className="coarse-table">
            <thead>
              <tr>
                <th>Label</th>
                <th>Score</th>
                <th>Wiki Link</th>
              </tr>
            </thead>
            <tbody>
              {topics.map((topic) => (
                <tr key={topic.id}>
                  <td>{topic.label}</td>
                  <td>{topic.score.toFixed(2)}</td>
                  <td>
                    <a href={topic.wikiLink} target="_blank" rel="noopener noreferrer">
                      {topic.wikiLink}
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {entities.length!=0 && (
        <div className="table-container">
          <h2>Entities</h2>
          <table className="coarse-table">
            <thead>
              <tr>
                <th>EntityID</th>
                <th>Confidence Score</th>
                <th>Relevance Score</th>
                <th>Wiki Link</th>
              </tr>
            </thead>
            <tbody>
              {entities.map((entity) => (
                <tr key={entity.id}>
                  <td>{entity.entityId}</td>
                  <td>{entity.confidenceScore.toFixed(2)}</td>
                  <td>{entity.relevanceScore.toFixed(2)}</td>
                  <td>
                    <a href={entity.wikiLink} target="_blank" rel="noopener noreferrer">
                      {entity.wikiLink}
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {keywords.length!=0 && (
        <div className="insert-keyword">
          <h2>Insert Keywords</h2>
          <p>Select from the listed keywords to insert</p>
          
          <div className='btn-keywords'>
            {keywords.map((keyword, index) => ( 
              <label> 
                {keyword}
                <input type="checkbox" name={keyword} value={keyword} onChange={toggleKeyword} />
              </label>
            ))}
          </div>

          <button onClick={handleInsertKeyword}>Insert</button>
        </div>
      )}


    </div>
  )
}

export default App
