import type { Brand, BrandCreate } from "../types/whey-protein";
import { httpClient, type ApiClient } from "./api.service";

export interface BrandRepository {
  getAll(): Promise<Brand[]>;
  getById(id: number): Promise<Brand>;
  create(data: BrandCreate): Promise<Brand>;
  update(id: number, data: BrandCreate): Promise<Brand>;
  delete(id: number): Promise<void>;
}

export class BrandService implements BrandRepository {
  apiClient: ApiClient;
  constructor(apiClient: ApiClient) {
    this.apiClient = apiClient;
  }

  async getAll(): Promise<Brand[]> {
    return this.apiClient.get<Brand[]>("/brands");
  }

  async getById(id: number): Promise<Brand> {
    return this.apiClient.get<Brand>(`/brands/${id}`);
  }

  async create(data: BrandCreate): Promise<Brand> {
    return this.apiClient.post<Brand>("/brands", data);
  }

  async update(id: number, data: BrandCreate): Promise<Brand> {
    return this.apiClient.put<Brand>(`/brands/${id}`, data);
  }

  async delete(id: number): Promise<void> {
    return this.apiClient.delete(`/brands/${id}`);
  }
}

export const brandService = new BrandService(httpClient);
