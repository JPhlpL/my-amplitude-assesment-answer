from fastapi import FastAPI, status, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

# User model
class User(BaseModel):
    username: str
    password: str

@app.get("/health-check")
async def health_check_endpoint() -> JSONResponse:
    return JSONResponse({"status": "up"})

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)