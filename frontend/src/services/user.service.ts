import { httpClient, type ApiClient } from "./api.service";

export interface UserCreate {
  name: string;
  email: string;
  plain_password: string;
  role?: "user" | "admin";
}

export interface UserRead {
  id: number;
  name: string;
  email: string;
  role: "user" | "admin";
}

export class UserService {
  apiClient: ApiClient;
  constructor(apiClient: ApiClient) {
    this.apiClient = apiClient;
  }

  async register(user: UserCreate): Promise<UserRead> {
    return this.apiClient.post<UserRead>("/users", user);
  }
}

export const userService = new UserService(httpClient);
