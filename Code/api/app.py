# Code/api/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# ---- CORS for frontend connection to API ----
app = FastAPI()

origins = [
    "http://localhost:5173",     # front end dev server
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- front_end/src/api/types.ts ----
class SolveRequest(BaseModel):
    problem: str

class SolveResponse(BaseModel):
    result: str
    error: str | None = None

# ---- sidebar class for endpoint ----
class SidebarItem(BaseModel):
    path: str
    label: str

class SidebarSection(BaseModel):
    title: Optional[str] = None
    items: List[SidebarItem]

class SidebarResponse(BaseModel):
    sections: List[SidebarSection]

# ---- useSolveProblem hook will call ----
@app.post("/solve", response_model=SolveResponse)
async def solve_problem(payload: SolveRequest) -> SolveResponse:
    # TODO: replace this with your real solver logic
    fake_solution = f"You asked me to solve: {payload.problem!r}"
    return SolveResponse(result=fake_solution)

@app.get("/")
def read_root():
    return {"message": "Optimus GPT backend is running"}

@app.get("/sidebar", response_model=SidebarResponse)
def get_sidebar():
    return SidebarResponse(
        sections=[
            SidebarSection(
                title="Navigation",
                items=[
                    SidebarItem(path="/", label="Home"),
                    SidebarItem(path="/settings", label="Settings"),
                ],
            ),
            SidebarSection(
                title="Resources",
                items=[
                    SidebarItem(path="/docs", label="API Docs (Swagger)"),
                ],
            ),
        ]
    )