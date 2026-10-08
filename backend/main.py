from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.setup import create_tables
from presentation.routes.task import router as task_router

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]) 
app.include_router(task_router, prefix="/api", tags=["tasks"])

create_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
