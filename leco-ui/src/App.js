import React, { useEffect, useState } from "react";
import axios from "axios";
import * as XLSX from "xlsx";
import Cookies from "js-cookie";
import "./App.css";

function App() {
  const [stationName, setStationName] = useState(Cookies.get("stationName") || "");
  const [file, setFile] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [additionalInfo, setAdditionalInfo] = useState(null);
  const [stationNames, setStationNames] = useState([]);

  useEffect(() => {
    const fetchStationNames = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/stations");
        setStationNames(response.data);
      } catch (error) {
        setErrorMessage("An error occurred while fetching station names.");
      }
    };

    fetchStationNames();
  }, []);

  const handleStationNameChange = (event) => {
    const selectedStation = event.target.value;
    setStationName(selectedStation);
    Cookies.set("stationName", selectedStation);
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async () => {
    setErrorMessage("");
    setAdditionalInfo(null); // Hide previous result

    if (!stationName) {
      setErrorMessage("Please select a station name.");
      return;
    }

    if (!file) {
      setErrorMessage("Please upload an Excel file.");
      return;
    }

    const formData = new FormData();
    formData.append("stationName", stationName);
    formData.append("locations", file);

    try {
      const response = await axios.post("http://127.0.0.1:8000/process/", formData);
      const data = response.data.data;
      setAdditionalInfo(response.data.info);
      createExcelFile(data);
    } catch (error) {
      setErrorMessage("An error occurred while processing the file.");
    }
  };

  const createExcelFile = (data) => {
    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
    XLSX.writeFile(wb, "processed_locations.xlsx");
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
      {additionalInfo && (
        <div>
          <h3>Additional Info</h3>
          <p>{additionalInfo.message}</p>
          <p>Total Distance: {additionalInfo.distance}</p>
          <p>
            Google Maps Route:{" "}
            <a href={additionalInfo.directions_url} target="_blank" rel="noreferrer">
              {additionalInfo.directions_url}
            </a>
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
