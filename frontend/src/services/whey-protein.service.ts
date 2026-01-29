import type {
  WheyProtein,
  WheyProteinCreate,
  WheyProteinRanking,
  RankingType,
} from "../types/whey-protein";
import { httpClient, type ApiClient } from "./api.service";

export interface WheyProteinRepository {
  getAll(): Promise<WheyProtein[]>;
  getById(id: number): Promise<WheyProtein>;
  create(data: WheyProteinCreate): Promise<WheyProtein>;
  update(id: number, data: WheyProteinCreate): Promise<WheyProtein>;
  delete(id: number): Promise<void>;
  getRanking(type: RankingType): Promise<WheyProteinRanking[]>;
}

export class WheyProteinService implements WheyProteinRepository {
  apiClient: ApiClient;
  constructor(apiClient: ApiClient) {
    this.apiClient = apiClient;
  }

  async getAll(): Promise<WheyProtein[]> {
    return this.apiClient.get<WheyProtein[]>("/whey");
  }

  async getById(id: number): Promise<WheyProtein> {
    return this.apiClient.get<WheyProtein>(`/whey/${id}`);
  }

  async create(data: WheyProteinCreate): Promise<WheyProtein> {
    return this.apiClient.post<WheyProtein>("/whey", data);
  }

  async update(id: number, data: WheyProteinCreate): Promise<WheyProtein> {
    return this.apiClient.put<WheyProtein>(`/whey/${id}`, data);
  }

  async delete(id: number): Promise<void> {
    return this.apiClient.delete(`/whey/${id}`);
  }

  async getRanking(type: RankingType): Promise<WheyProteinRanking[]> {
    return this.apiClient.get<WheyProteinRanking[]>(
      `/whey/rankings/${type}`
    );
  }
}

export const wheyProteinService = new WheyProteinService(httpClient);
