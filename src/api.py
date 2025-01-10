from fastapi import FastAPI
from insight_generator import generate_insights

app = FastAPI()

@app.get("/insights")
async def get_insights():
    return {"insights": generate_insights()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 