# Code/api/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ---- CORS for frontend connection to API ----
app = FastAPI()

origins = [
    "http://localhost:5173",     # front end dev server
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health check ---
@app.get("/health")
async def health():
    return {"status": "ok"}

# ---- front_end/src/api/types.ts ----
class SolveRequest(BaseModel):
    problem: str

class SolveResponse(BaseModel):
    result: str
    error: str | None = None

# ---- useSolveProblem hook will call ----
@app.post("/solve", response_model=SolveResponse)
async def solve_problem(payload: SolveRequest) -> SolveResponse:
    # TODO: replace this with your real solver logic
    fake_solution = f"You asked me to solve: {payload.problem!r}"
    return SolveResponse(result=fake_solution)
