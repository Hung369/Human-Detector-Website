import { useState } from 'react'
import Link from 'next/link'
import axios from 'axios'

export default function Home() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  
  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleUpload = async () => {
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    try {
      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setResult(response.data)
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div style={{ padding: '20px' }}>
      <h1>Upload Image for Person Detection</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>

      <div style={{ marginTop: '10px' }}>
        <Link href="/history">
          <button>Go to History</button>
        </Link>
      </div>

      {result && (
        <div>
          <h2>Detection Result</h2>
          <p>Number of persons: {result.num_people}</p>
          <img src={`http://localhost:8000/${result.image_path}`}
            alt="Detection Result" 
            style={{ maxWidth: '100%', height: 'auto' }} 
          />
        </div>
      )}
    </div>
  )
}
