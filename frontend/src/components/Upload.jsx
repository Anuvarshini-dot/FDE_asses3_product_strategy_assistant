import { useState } from 'react'

export default function Upload({ backend, onStatus, onUploadSuccess }) {
  const [files, setFiles] = useState([])
  const [uploading, setUploading] = useState(false)

  const handleUpload = async () => {
    setUploading(true)
    try {
      const formData = new FormData()
      Array.from(files).forEach(file => formData.append('files', file))
      const res = await fetch(backend + '/upload', {
        method: 'POST',
        body: formData,
      })
      if (res.ok) {
        onStatus('Uploaded ' + files.length + ' file(s) successfully.')
        setFiles([])
        onUploadSuccess()
      } else {
        const err = await res.json().catch(() => ({ detail: res.statusText }))
        onStatus('Error: ' + (err.detail || res.statusText))
      }
    } catch (e) {
      onStatus('Error: ' + e.message)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="upload-section">
      <h3>Upload Documents</h3>
      <p className="upload-hint">TXT, PDF, CSV, JSON</p>
      <label className="file-label">
        <input
          type="file"
          multiple
          accept=".txt,.pdf,.csv,.json"
          style={{ display: 'none' }}
          onChange={e => setFiles(e.target.files)}
        />
        Choose Files
      </label>
      {files.length > 0 && (
        <div className="file-list">
          {Array.from(files).map(file => (
            <span className="file-chip" key={file.name}>{file.name}</span>
          ))}
          <button
            className="btn-secondary"
            onClick={handleUpload}
            disabled={uploading}
          >
            {uploading ? 'Uploading...' : 'Upload ' + files.length + ' file(s)'}
          </button>
        </div>
      )}
    </div>
  )
}
