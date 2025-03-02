import { useEffect, useState } from 'react'
import axios from 'axios'

export default function History() {
  const [records, setRecords] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  
  // These are the active search parameters used in fetchHistory.
  const [search, setSearch] = useState('')
  const [startTime, setStartTime] = useState('')
  const [endTime, setEndTime] = useState('')

  // These hold the input values for the search form.
  const [searchInput, setSearchInput] = useState('')
  const [startTimeInput, setStartTimeInput] = useState('')
  const [endTimeInput, setEndTimeInput] = useState('')

  const fetchHistory = async (page, search, startTime, endTime) => {
    try {
      const skip = (page - 1) * 10;
      const params = { skip, limit: 10 };
      if (search.trim() !== '') params.search = search;
      if (startTime.trim() !== '') params.start_time = startTime;
      if (endTime.trim() !== '') params.end_time = endTime;

      const response = await axios.get('http://localhost:8000/history/', { params });
      setRecords(response.data.records);
      setTotal(response.data.total);
    } catch (error) {
      console.error(error);
    }
  }

  // useEffect will only trigger fetchHistory when the active search parameters change
  useEffect(() => {
    fetchHistory(page, search, startTime, endTime);
  }, [page, search, startTime, endTime]);

  const handleSearch = (e) => {
    e.preventDefault();
    // Update the active search parameters only when the search button is pressed.
    setSearch(searchInput);
    setStartTime(startTimeInput);
    setEndTime(endTimeInput);
    setPage(1);
    // Optionally, trigger a fetch immediately:
    fetchHistory(1, searchInput, startTimeInput, endTimeInput);
  }

  const handleReset = () => {
    // Clear both the input fields and the active search parameters.
    setSearchInput('');
    setStartTimeInput('');
    setEndTimeInput('');
    setSearch('');
    setStartTime('');
    setEndTime('');
    setPage(1);
    fetchHistory(1, '', '', '');
  }

  return (
    <div style={{ padding: '20px' }}>
      <button onClick={() => window.location.href = '/'}>Back to Index</button>
      <h1>Detection History</h1>
      <form onSubmit={handleSearch}>
        <div>
          <input 
            type="text" 
            value={searchInput} 
            onChange={(e) => setSearchInput(e.target.value)}
            placeholder="Search by image name" 
          />
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>
            Start Date & Time: 
            <input 
              type="datetime-local"
              value={startTimeInput}
              onChange={(e) => setStartTimeInput(e.target.value)}
            />
          </label>
        </div>
        <div style={{ marginTop: '10px' }}>
          <label>
            End Date & Time: 
            <input 
              type="datetime-local"
              value={endTimeInput}
              onChange={(e) => setEndTimeInput(e.target.value)}
            />
          </label>
        </div>
        <div style={{ marginTop: '10px' }}>
          <button type="submit">Search</button>
          <button type="button" onClick={handleReset} style={{ marginLeft: '10px' }}>
            Reset
          </button>
        </div>
      </form>
      <table border="1" cellPadding="10" style={{ marginTop: '20px' }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Timestamp</th>
            <th>Detected Count</th>
            <th>Image</th>
          </tr>
        </thead>
        <tbody>
          {records.map(record => (
            <tr key={record.id}>
              <td>{record.id}</td>
              <td>{new Date(record.timestamp).toLocaleString()}</td>
              <td>{record.num_people}</td>
              <td>
                <img 
                  src={`http://localhost:8000/${record.image_path}`} 
                  alt="result" 
                  style={{ width: '100px' }} 
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ marginTop: '20px' }}>
        <button disabled={page === 1} onClick={() => setPage(page - 1)}>Previous</button>
        <span style={{ margin: '0 10px' }}>Page {page}</span>
        <button disabled={page * 10 >= total} onClick={() => setPage(page + 1)}>Next</button>
      </div>
    </div>
  )
}
