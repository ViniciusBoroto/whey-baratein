import { useState, useEffect } from "react";
import type {
  WheyProtein,
  WheyProteinRanking,
  RankingType,
} from "../types/whey-protein";
import type { WheyProteinRepository } from "../services/whey-protein.service";

interface UseAsyncState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

export function useWheyProteins(
  repository: WheyProteinRepository
): UseAsyncState<WheyProtein[]> {
  const [state, setState] = useState<UseAsyncState<WheyProtein[]>>({
    data: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        setState((prev) => ({ ...prev, loading: true, error: null }));
        const data = await repository.getAll();
        setState({ data, loading: false, error: null });
      } catch (error) {
        setState({
          data: null,
          loading: false,
          error: error instanceof Error ? error.message : "Unknown error",
        });
      }
    };

    fetchData();
  }, [repository]);

  return state;
}

export function useWheyProteinRanking(
  repository: WheyProteinRepository,
  type: RankingType
): UseAsyncState<WheyProteinRanking[]> {
  const [state, setState] = useState<UseAsyncState<WheyProteinRanking[]>>({
    data: null,
    loading: true,
    error: null,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        setState((prev) => ({ ...prev, loading: true, error: null }));
        const data = await repository.getRanking(type);
        setState({ data, loading: false, error: null });
      } catch (error) {
        setState({
          data: null,
          loading: false,
          error: error instanceof Error ? error.message : "Unknown error",
        });
      }
    };

    fetchData();
  }, [repository, type]);

  return state;
}
