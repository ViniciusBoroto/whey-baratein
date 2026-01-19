import { PiQuestionBold } from "react-icons/pi";
import type { WheyProtein } from "../types/whey-protein";
import { Tooltip } from "./Tooltip";

export interface WheyCardProps {
  whey: WheyProtein;
}

export const WheyCard: React.FC<WheyCardProps> = ({ whey }) => {
  return (
    <div className="flex justify-between align-middle h-60 w-full bg-surface-alt shadow-lg drop-shadow-brand rounded-base overflow-visible hover:shadow-xl hover:scale-103 transition duration-300 ease-in-out hover:-translate-y-1">
      <div className="h-full w-2/5 object-cover drop-shadow-xl drop-shadow-border rounded-l-base overflow-hidden">
        <img
          src={whey?.image_url || "https://placehold.co/500x600"}
          alt=""
          className="h-full w-full object-cover"
        />
      </div>
      <div className="w-3/5 h-full bg-surface-alt p-4 flex flex-col justify-between">
        <div>
          <h2 className="text-lg ">{whey.name}</h2>
          <div className="flex items-center">
            <img
              src={whey.brand?.logo_url || "https://placehold.co/50x50"}
              className="inline rounded-full w-8 mr-2 my-1 drop-shadow-md drop-shadow-border"
              alt=""
            />
            <span className="text-md">{whey.brand?.name || "Sem marca"}</span>
          </div>
        </div>
        <div>
          <p>
            Preço por EAA:{" "}
            {whey.eea_per_serving === 0 ? (
              <Tooltip text="Aminograma não cadastrado">
                <span className="bg-surface font-extrabold text-heading text-shadow-2xs text-shadow-default inline-flex items-center justify-center shadow-md shadow-border-medium p-2 rounded-full">
                  <PiQuestionBold className="text-body" />
                </span>
              </Tooltip>
            ) : (
              <span className="bg-surface font-extrabold text-heading text-shadow-2xs text-shadow-default inline-flex items-center justify-center shadow-md shadow-border border border-border p-2 rounded-full">
                {"R$" +
                  whey.eea_per_serving.toFixed(2).toString().replace(".", ",")}
              </span>
            )}
          </p>
        </div>
        <div>
          <p>
            Preço:{" "}
            <span className="font-bold">
              {"R$" + whey.price.toFixed(2).toString().replace(".", ",")}
            </span>
            <br />
            Concentração:{" "}
            <span className="font-bold">
              {whey.protein_concentration.toFixed(2)}%
            </span>
          </p>
        </div>
      </div>
    </div>
  );
};
