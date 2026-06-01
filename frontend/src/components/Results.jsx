import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeRaw from 'rehype-raw'

const SECTIONS = [
  { key: 'customer_insights',  label: 'Customer Insights',           color: '#f59e0b' },
  { key: 'market_insights',    label: 'Market & Competitor Analysis', color: '#3b82f6' },
  { key: 'feature_priorities', label: 'Feature Prioritization',      color: '#8b5cf6' },
  { key: 'swot_analysis',      label: 'SWOT Analysis',               color: '#10b981' },
  { key: 'executive_summary',  label: 'Executive Summary',           color: '#6366f1' },
]

export default function Results({ results }) {
  if (!results) {
    return (
      <div className="results-grid">
        <div className="empty-state">
          <div className="empty-state-graphic">
            <div className="empty-bar" style={{ height: '20px' }} />
            <div className="empty-bar" style={{ height: '32px' }} />
            <div className="empty-bar" style={{ height: '14px' }} />
            <div className="empty-bar" style={{ height: '28px' }} />
          </div>
          <p>Upload your product documents and click <strong>Run Analysis</strong> to generate AI-powered strategic insights across 5 dimensions.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="results-grid">
      {SECTIONS.map(({ key, label, color }) =>
        results[key] ? (
          <div key={key} className={"card" + (key === 'executive_summary' ? ' card-full' : '')}>
            <div className="card-header">
              <div className="card-accent" style={{ background: color }} />
              <h3 className="card-title">{label}</h3>
            </div>
            <div className="card-body">
              <ReactMarkdown className="md" remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>{results[key]}</ReactMarkdown>
            </div>
          </div>
        ) : null
      )}
    </div>
  )
}
