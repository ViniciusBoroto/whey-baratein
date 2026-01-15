import "./App.css";
import { DarkModeButton } from "./components/DarkModeButton";
import logo from "./../public/whey-baratein.png";

function App() {
  return (
    <>
      <header className="flex sticky top-0 z-10 bg-surface-strong items-center justify-between h-25 shadow-2xs shadow-surface-alt rounded-base p-5">
        <a className="w-50 text-shadow-2xl">
          <img src={logo} alt="Whey Baratein" className="-ml-10 mt-1" />
        </a>
        <div className="h-auto">
          <DarkModeButton></DarkModeButton>
        </div>
      </header>
      <main className="flex flex-col items-center justify-center h-screen ">
        {/* CARD */}
        <div className="h-25 w-50 bg-surface-alt"></div>
      </main>
      <footer>Footer</footer>
    </>
  );
}

export default App;
