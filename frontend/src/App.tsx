import "./App.css";
import { DarkModeButton } from "./components/DarkModeButton";
import logo from "./../public/whey-baratein.png";

function App() {
  return (
    <>
      <header className="sticky top-0 z-40 flex-none w-full mx-auto bg-neutral-primary border-b border-border-light">
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
          <div className="h-auto">
            <DarkModeButton></DarkModeButton>
          </div>
        </div>
      </header>
      <main className="p-10">
        <div className="grid grid-cols-3 gap-7">
          <div className="flex justify-between align-middle h-80 w-full bg-surface-alt shadow-xl drop-shadow-brand rounded-2xl overflow-hidden">
            <img
              src="https://placehold.co/500x600"
              className="w-2/5 h-full object-cover drop-shadow-xl drop-shadow-border"
              alt=""
            />
            <div className="w-full h-full bg-surface-alt p-6 flex flex-col justify-between">
              <div>
                <h2 className="text-3xl ">Whey 100% 3W Hidrolisado</h2>
                <div className="flex items-center">
                  <img
                    src="https://placehold.co/50x50"
                    className="inline rounded-full w-10 mr-2 my-2 drop-shadow-md drop-shadow-border"
                    alt=""
                  />
                  <span className="text-md">Marca</span>
                </div>
              </div>
              <div>
                <p>
                  Preço por EAA:{" "}
                  <span className="bg-surface font-extrabold text-heading text-shadow-2xs text-shadow-default inline-block shadow-md shadow-border border border-border p-2 rounded-full">
                    R$ 0,53
                  </span>
                </p>
              </div>
              <div>
                <p>
                  Preço: <span className="font-bold">R$ 90,00</span>
                  <br />
                  Concentração: <span className="font-bold">00%</span>
                </p>
              </div>
            </div>
          </div>
          <div className="h-80 w-full bg-surface-alt"></div>
          <div className="h-80 w-full bg-surface-alt"></div>
        </div>
      </main>
      <footer>Footer</footer>
    </>
  );
}

export default App;
