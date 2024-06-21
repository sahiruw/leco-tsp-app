import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [stationName, setStationName] = useState('');
  const [file, setFile] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [downloadLink, setDownloadLink] = useState('');

  const [stationNames, setStationNames] = useState([]);


  useEffect(() => {
    let res = axios.get('http://127.0.0.1:8000/stations');
    res.then(res => {
      console.log(res.data);
      setStationNames(res.data);
    });
  }
  , []);

  const handleStationNameChange = (event) => {
    setStationName(event.target.value);
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async () => {
    setErrorMessage('');

    if (!stationName) {
      setErrorMessage('Please select a station name.');
      return;
    }

    if (!file) {
      setErrorMessage('Please upload an Excel file.');
      return;
    }

    const formData = new FormData();
    formData.append('stationName', stationName);
    formData.append('locations', file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/process/', formData, {
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      setDownloadLink(url);
    } catch (error) {
      setErrorMessage('An error occurred while processing the file.');
    }
  };

  return (
    <div className="App">
      <h1>Upload Excel File</h1>
      <div>
        <label>
          Station Name:
          <select value={stationName} onChange={handleStationNameChange}>
            <option value="">Select a station</option>
            {stationNames.map((name) => (
              <option key={name} value={name}>
                {name}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div>
        <label>
          Upload Excel File:
          <input type="file" accept=".xlsx, .xls" onChange={handleFileChange} />
        </label>
      </div>
      {errorMessage && <p className="error">{errorMessage}</p>}
      <button onClick={handleSubmit}>Upload and Process</button>
      {downloadLink && (
        <div>
          <a href={downloadLink} download="processed_locations.xlsx">
            Download Processed File
          </a>
        </div>
      )}
    </div>
  );
}

export default App;
