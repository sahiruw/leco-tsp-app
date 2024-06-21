from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import BytesIO

from distance import get_all_station_names
from process import process_file

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # React app default port
    "http://localhost:3001",  # Alternative React app port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/process/")
async def process_excel(
        stationName: str = Form(...),
        locations: UploadFile = File(...)
):
    try:
        # Read the uploaded file into a bytes buffer
        file_content = await locations.read()
        file_buffer = BytesIO(file_content)

        # Read the buffer into a Pandas DataFrame
        df = pd.read_excel(file_buffer)

        # Add a new column with the station name
        data, distance, directions_url = process_file(df, stationName)

        # Example additional text values to return
        additional_info = {
            "message": "File processed successfully",
            "distance": distance,
            "directions_url": directions_url
        }

        response = {
            "data": data,
            "info": additional_info
        }

        return JSONResponse(content=response)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



@app.get("/stations")
async def get_stations():
    try:
        return get_all_station_names()
    except Exception as e:
        return []


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)