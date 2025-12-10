import { useMutation } from "@tanstack/react-query";
import { api } from "./client";
import { SolveRequest, SolveResponse } from "./types";

export function useSolveProblem() {
  return useMutation({
    mutationFn: async (payload: SolveRequest) => {
      const res = await api.post<SolveResponse>("/solve", payload);
      return res.data;
    },
  });
}