from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
import pandas as pd
from io import BytesIO

app = FastAPI()


@app.post("/process/")
async def process_excel(
        stationName: str = Form(...),
        locations: UploadFile = File(...)
):
    # Read the uploaded file into a bytes buffer
    file_content = await locations.read()
    file_buffer = BytesIO(file_content)

    # Read the buffer into a Pandas DataFrame
    df = pd.read_excel(file_buffer)

    # Add a new column with the station name
    df['StationName'] = stationName

    # Save the modified DataFrame to a new Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    # Return the processed file using StreamingResponse
    headers = {
        'Content-Disposition': 'attachment; filename="processed_locations.xlsx"',
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
    return StreamingResponse(output, headers=headers)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
