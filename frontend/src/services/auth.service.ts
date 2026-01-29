import { httpClient, type ApiClient } from "./api.service";

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export class AuthService {
  apiClient: ApiClient;
  constructor(apiClient: ApiClient) {
    this.apiClient = apiClient;
  }

  async login(credentials: LoginRequest): Promise<TokenResponse> {
    const response = await this.apiClient.post<TokenResponse>("/auth/login", credentials);
    this.apiClient.setAuthToken(response.access_token);
    return response;
  }

  logout(): void {
    this.apiClient.setAuthToken(null);
  }
}

export const authService = new AuthService(httpClient);
