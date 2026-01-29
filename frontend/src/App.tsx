import "./App.css";
import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { DarkModeButton } from "./components/DarkModeButton";
import logo from "./../public/whey-baratein.png";
import { HomePage } from "./pages/HomePage";
import { AuthPage } from "./pages/AuthPage";
import { PrimaryButton } from "./components/PrimaryButton";
import { useState } from "react";
import { CreateWheyProteinModal } from "./components/CreateWheyProteinModal";

function AppContent() {
  const [isCreating, setIsCreating] = useState(false);
  const { isAuthenticated, logout } = useAuth();
  const location = useLocation();
  const isAuthPage = location.pathname === "/auth";

  if (isAuthPage) {
    return (
      <Routes>
        <Route path="/auth" element={isAuthenticated ? <Navigate to="/" /> : <AuthPage />} />
      </Routes>
    );
  }

  return (
    <>
      <CreateWheyProteinModal
        isOpen={isCreating}
        onClose={() => setIsCreating(false)}
      />
      <header className="sticky top-0 z-40 flex-none w-full mx-auto bg-neutral-primary border-b border-border-medium">
        <div className="flex items-center justify-between w-full px-3 py-3 mx-auto bg-surface">
          <div className="flex items-center max-h-14 max-w-40 overflow-hidden">
            <a className="w-max h-max text-shadow-2xl overflow-hidden cursor-pointer">
              <img
                src={logo}
                alt="Whey Baratein"
                className="w-full h-full object-contain -ml-9"
              />
            </a>
          </div>
          <div className="h-auto flex items-center gap-3">
            <DarkModeButton />
            {isAuthenticated ? (
              <>
                <PrimaryButton onClick={() => setIsCreating(true)}>
                  + Adicionar
                </PrimaryButton>
                <PrimaryButton onClick={logout}>Logout</PrimaryButton>
              </>
            ) : (
              <PrimaryButton onClick={() => window.location.href = "/auth"}>
                Login / Signup
              </PrimaryButton>
            )}
          </div>
        </div>
      </header>
      <main className="p-10">
        <Routes>
          <Route path="/" element={<HomePage />} />
        </Routes>
      </main>
      <footer>Footer</footer>
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
