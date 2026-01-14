import type { Brand, BrandCreate } from "../types/whey-protein";
import { httpClient, type ApiClient } from "./api.service";

export interface BrandRepository {
  getAll(): Promise<Brand[]>;
  create(data: BrandCreate): Promise<Brand>;
}
export class BrandService implements BrandRepository {
  apiClient: ApiClient;
  constructor(apiClient: ApiClient) {
    this.apiClient = apiClient;
  }

  async getAll(): Promise<Brand[]> {
    return this.apiClient.get<Brand[]>("/brands/");
  }

  async getById(id: number): Promise<Brand> {
    return this.apiClient.get<Brand>(`/brands/${id}`);
  }

  async create(data: BrandCreate): Promise<Brand> {
    return this.apiClient.post<Brand>("/brands/", data);
  }
}

export const brandService = new BrandService(httpClient);
