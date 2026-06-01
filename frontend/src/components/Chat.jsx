import { useRef, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeRaw from 'rehype-raw'

export default function Chat({ backend }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  const send = async () => {
    const text = input.trim()
    if (!text || loading) return
    const history = [...messages]
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: text }])
    setLoading(true)
    try {
      const response = await fetch(backend + '/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, history }),
      })
      const data = await response.json()
      const content = data.response || data.detail || 'No response received.'
      setMessages(prev => [...prev, { role: 'assistant', content }])
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: err.message || 'An error occurred.' }])
    } finally {
      setLoading(false)
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.length === 0 && (
          <p className="chat-hint">Ask anything about your product strategy...</p>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={"message " + msg.role}>
            <span className="msg-label">{msg.role === 'user' ? 'You' : 'Assistant'}</span>
            {msg.role === 'assistant'
              ? <ReactMarkdown className="md" remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}>{msg.content}</ReactMarkdown>
              : <p>{msg.content}</p>
            }
          </div>
        ))}
        {loading && (
          <div className="message assistant">
            <span className="msg-label">Assistant</span>
            <p className="typing">Thinking...</p>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
      <div className="chat-input">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send() } }}
          placeholder="Ask about your product strategy..."
          disabled={loading}
        />
        <button className="btn-primary" onClick={send} disabled={loading || !input.trim()}>Send</button>
      </div>
    </div>
  )
}
