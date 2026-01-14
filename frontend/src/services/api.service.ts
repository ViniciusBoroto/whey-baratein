export interface ApiClient {
  get<T>(url: string): Promise<T>;
  post<T>(url: string, data: unknown): Promise<T>;
  put<T>(url: string, data: unknown): Promise<T>;
  delete(url: string): Promise<void>;
}

export class HttpClient implements ApiClient {
  private baseURL: string;

  constructor(baseURL: string = "http://localhost:8000") {
    this.baseURL = baseURL;
  }

  async get<T>(url: string): Promise<T> {
    const response = await fetch(`${this.baseURL}${url}`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
  }

  async post<T>(url: string, data: unknown): Promise<T> {
    const response = await fetch(`${this.baseURL}${url}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
  }

  async put<T>(url: string, data: unknown): Promise<T> {
    const response = await fetch(`${this.baseURL}${url}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return response.json();
  }

  async delete(url: string): Promise<void> {
    const response = await fetch(`${this.baseURL}${url}`, {
      method: "DELETE",
    });
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
  }
}

export const httpClient = new HttpClient();
