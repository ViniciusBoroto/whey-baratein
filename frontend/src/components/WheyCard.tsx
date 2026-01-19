import { PiMoneyWavyBold, PiMoneyWavyDuotone } from "react-icons/pi";

export const WheyCard = () => {
  return (
    <div className="flex justify-between align-middle h-60 w-full bg-surface-alt shadow-lg drop-shadow-brand rounded-2xl overflow-hidden hover:shadow-xl hover:scale-103 transition duration-300 ease-in-out hover:-translate-y-1">
      <img
        src="https://placehold.co/500x600"
        className="w-2/5 h-full object-cover drop-shadow-xl drop-shadow-border"
        alt=""
      />
      <div className="w-full h-full bg-surface-alt p-4 flex flex-col justify-between">
        <div>
          <h2 className="text-lg ">Whey 100% 3W Hidrolisado</h2>
          <div className="flex items-center">
            <img
              src="https://placehold.co/50x50"
              className="inline rounded-full w-8 mr-2 my-1 drop-shadow-md drop-shadow-border"
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
  );
};
