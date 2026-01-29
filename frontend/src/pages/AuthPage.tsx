import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { userService } from "../services/user.service";
import { Input } from "../components/Input";
import { PrimaryButton } from "../components/PrimaryButton";
import logo from "./../../public/whey-baratein.png";

export const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      if (isLogin) {
        await login(email, password);
        navigate("/");
      } else {
        await userService.register({ name, email, plain_password: password });
        await login(email, password);
        navigate("/");
      }
    } catch (err) {
      setError(isLogin ? "Invalid credentials" : "Registration failed");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-surface">
      <div className="bg-neutral-primary p-8 rounded-lg border border-border-medium w-full max-w-md">
        <h1 className="flex items-center justify-center w-full h-50 -mt-8"><img className="h-full " src={logo} alt="" /></h1>

        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setIsLogin(true)}
            className={`flex-1 py-2 rounded ${isLogin ? "bg-primary text-white border-b border-border" : "bg-surface"}`}
          >
            Login
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`flex-1 py-2 rounded ${!isLogin ? "bg-primary text-white border-b border-border" : "bg-surface"}`}
          >
            Register
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {!isLogin && (
            <Input
              id="name"
              label="Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          )}
          <Input
            id="email"
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <Input
            id="password"
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <PrimaryButton type="submit" className="w-full">
            {isLogin ? "Login" : "Register"}
          </PrimaryButton>
        </form>
      </div>
    </div>
  );
};
