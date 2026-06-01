import { useState, useEffect } from 'react'
import Upload from './components/Upload'
import Results from './components/Results'
import Chat from './components/Chat'
import Report from './components/Report'

const BACKEND = import.meta.env.VITE_BACKEND_URL || ''

export default function App() {
  const [tab, setTab] = useState('results')
  const [status, setStatus] = useState('')
  const [analyzing, setAnalyzing] = useState(false)
  const [results, setResults] = useState(null)
  const [docs, setDocs] = useState([])

  async function refreshDocs() {
    try {
      const r = await fetch(BACKEND + '/documents')
      if (r.ok) {
        const data = await r.json()
        setDocs(data.documents)
      }
    } catch {
      // backend may not be ready yet
    }
  }

  useEffect(() => {
    refreshDocs()
  }, [])

  async function runAnalysis() {
    setAnalyzing(true)
    setStatus('Running 5 AI agents...')
    try {
      const res = await fetch(BACKEND + '/analyze', { method: 'POST' })
      if (res.ok) {
        const data = await fetch(BACKEND + '/results')
        const json = await data.json()
        setResults(json)
        setTab('results')
        setStatus('Analysis complete!')
      } else {
        const err = await res.json().catch(() => ({}))
        setStatus(err.detail || 'Analysis failed.')
      }
    } catch (e) {
      setStatus(e.message || 'An error occurred.')
    } finally {
      setAnalyzing(false)
    }
  }

  async function handleReset() {
    await fetch(BACKEND + '/reset', { method: 'DELETE' })
    setResults(null)
    setDocs([])
    setStatus('Reset complete')
  }

  return (
    <div className="app">
      <header>
        <div className="header-icon">PS</div>
        <div className="header-content">
          <h1>Product Strategy Assistant</h1>
          <p>Multi-agent AI powered strategic insights</p>
        </div>
      </header>
      <div className="layout">
        <aside>
          <Upload backend={BACKEND} onStatus={setStatus} onUploadSuccess={refreshDocs} />

          <div className="doc-list">
            <h4>Documents {docs.length > 0 ? "(" + docs.length + ")" : ""}</h4>
            {docs.length === 0 ? (
              <p className="no-docs">No documents uploaded yet</p>
            ) : (
              docs.map((name, i) => (
                <span key={i} className="doc-item" title={name}>{name}</span>
              ))
            )}
          </div>

          <div className="sidebar-actions">
            <button
              className="btn-primary"
              onClick={runAnalysis}
              disabled={analyzing || docs.length === 0}
            >
              {analyzing ? 'Analyzing...' : 'Run Analysis'}
            </button>
            <button className="btn-ghost" onClick={handleReset}>
              Reset All
            </button>
          </div>

          {status && <p className="status-msg">{status}</p>}
        </aside>

        <main>
          <div className="tabs">
            <button className={"tab-btn" + (tab === 'results' ? ' active' : '')} onClick={() => setTab('results')}>Results</button>
            <button className={"tab-btn" + (tab === 'chat' ? ' active' : '')} onClick={() => setTab('chat')}>Chat</button>
            <button className={"tab-btn" + (tab === 'report' ? ' active' : '')} onClick={() => setTab('report')}>Report</button>
          </div>
          <div className="tab-content">
            {tab === 'results' && <Results results={results} />}
            {tab === 'chat' && <Chat backend={BACKEND} />}
            {tab === 'report' && <Report backend={BACKEND} />}
          </div>
        </main>
      </div>
    </div>
  )
}
