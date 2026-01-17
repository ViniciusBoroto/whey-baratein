import "./App.css";
import { DarkModeButton } from "./components/DarkModeButton";
import logo from "./../public/whey-baratein.png";
import { HomePage } from "./pages/HomePage";
import { PrimaryButton } from "./components/PrimaryButton";
import { useState } from "react";
import { CreateWheyProteinModal } from "./components/CreateWheyProteinModal";

function App() {
  const [isCreating, setIsCreating] = useState(false);
  return (
    <>
      <CreateWheyProteinModal
        isOpen={isCreating}
        onClose={() => setIsCreating(false)}
      ></CreateWheyProteinModal>
      <header className="sticky top-0 z-40 flex-none w-full mx-auto bg-neutral-primary border-b border-border-medium">
        {/* Top Bar */}
        <div className="flex items-center justify-between w-full px-3 py-3 mx-auto bg-surface">
          {/* Left part of top bar */}
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
            <DarkModeButton></DarkModeButton>
            <PrimaryButton onClick={() => setIsCreating(true)}>
              + Adicionar
            </PrimaryButton>
          </div>
        </div>
      </header>
      <main className="p-10">
        <HomePage></HomePage>
      </main>
      <footer>Footer</footer>
    </>
  );
}

export default App;
