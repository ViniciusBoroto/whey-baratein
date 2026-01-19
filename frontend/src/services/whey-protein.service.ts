import { WheyProtein, WheyProteinCreate, WheyProteinRanking, RankingType } from '../types/whey-protein';

export interface ApiClient {
  get<T>(url: string): Promise<T>;
  post<T>(url: string, data: unknown): Promise<T>;
  put<T>(url: string, data: unknown): Promise<T>;
  delete(url: string): Promise<void>;
}

export interface WheyProteinRepository {
  getAll(): Promise<WheyProtein[]>;
  getById(id: number): Promise<WheyProtein>;
  create(data: WheyProteinCreate): Promise<WheyProtein>;
  update(id: number, data: WheyProteinCreate): Promise<WheyProtein>;
  delete(id: number): Promise<void>;
  getRanking(type: RankingType): Promise<WheyProteinRanking[]>;
}

class HttpClient implements ApiClient {
  private baseURL: string;

  constructor(baseURL: string = 'http://localhost:8000') {
    this.baseURL = baseURL;
  }

  async get<T>(url: string): Promise<T> {
    const response = await fetch(`${this.baseURL}${url}`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
  }

  async post<T>(url: string, data: unknown): Promise<T> {
    const response = await fetch(`${this.baseURL}${url}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
  }

  async put<T>(url: string, data: unknown): Promise<T> {
    const response = await fetch(`${this.baseURL}${url}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
  }

  async delete(url: string): Promise<void> {
    const response = await fetch(`${this.baseURL}${url}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  }
}

export class WheyProteinService implements WheyProteinRepository {
  constructor(private apiClient: ApiClient) {}

  async getAll(): Promise<WheyProtein[]> {
    return this.apiClient.get<WheyProtein[]>('/whey-proteins/');
  }

  async getById(id: number): Promise<WheyProtein> {
    return this.apiClient.get<WheyProtein>(`/whey-proteins/${id}`);
  }

  async create(data: WheyProteinCreate): Promise<WheyProtein> {
    return this.apiClient.post<WheyProtein>('/whey-proteins/', data);
  }

  async update(id: number, data: WheyProteinCreate): Promise<WheyProtein> {
    return this.apiClient.put<WheyProtein>(`/whey-proteins/${id}`, data);
  }

  async delete(id: number): Promise<void> {
    return this.apiClient.delete(`/whey-proteins/${id}`);
  }

  async getRanking(type: RankingType): Promise<WheyProteinRanking[]> {
    return this.apiClient.get<WheyProteinRanking[]>(`/whey-proteins/rankings/${type}`);
  }
}

export const httpClient = new HttpClient();
export const wheyProteinService = new WheyProteinService(httpClient);