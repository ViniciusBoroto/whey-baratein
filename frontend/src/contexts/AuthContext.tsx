import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { authService } from "../services/auth.service";

interface AuthContextType {
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token")
  );

  useEffect(() => {
    if (token) {
      localStorage.setItem("token", token);
      authService.apiClient.setAuthToken(token);
    } else {
      localStorage.removeItem("token");
      authService.apiClient.setAuthToken(null);
    }
  }, [token]);

  const login = async (email: string, password: string) => {
    const response = await authService.login({ email, password });
    setToken(response.access_token);
  };

  const logout = () => {
    authService.logout();
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
};
