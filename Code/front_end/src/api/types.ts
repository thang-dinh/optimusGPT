export interface SolveRequest {
  problem: string;
}

export interface SolveResponse {
  result: string; // summary text returned by FastAPI
  error?: string; // when request fails
}