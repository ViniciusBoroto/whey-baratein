import type { WheyProtein } from "../types/whey-protein";
import { Card } from "./Card";
import { StarArray } from "./StarArray";

interface WheyProteinEditableCardProps {
  wheyProtein: WheyProtein;
  darkMode: boolean;
  onEdit: (wheyProtein: WheyProtein) => void;
  onDelete: (wheyProteinId: number) => void;
}

export const WheyProteinEditableCard: React.FC<
  WheyProteinEditableCardProps
> = ({ wheyProtein, darkMode, onEdit, onDelete }) => {
  return (
    <>
      <Card key={wheyProtein.id} className="flex justify-between">
        {/* Left (photo)*/}
        <img
          src={
            wheyProtein.image_url
              ? wheyProtein.image_url
              : "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/1665px-No-Image-Placeholder.svg.png"
          }
          alt={wheyProtein.name}
          className="w-50 basis-1 h-auto object-cover rounded mb-2"
        />
        {/* Right */}
        <div className="flex flex-col w-full h-full ml-4 justify-center">
          <div className="mb-2 flex-1">
            <h3 className="text-xs font-semibold truncate">
              {wheyProtein.name}
            </h3>
            <p
              className={`text-xs ${
                darkMode ? "text-gray-400" : "text-gray-600"
              }`}
            >
              {wheyProtein.brand?.name || "Sem marca"}
            </p>
          </div>
          <div className="flex items-center justify-between mb-2 flex-1">
            <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded">
              R$ {wheyProtein.price.toFixed(2).toString().replace(".", ",")}
            </span>
            <StarArray filledStars={wheyProtein.reliability} length={5} />
          </div>

          <div className="space-y-1 mb-2 text-xs">
            <div className="flex justify-between">
              <span
                className={`${darkMode ? "text-gray-400" : "text-gray-600"}`}
              >
                Proteína:
              </span>
              <span className="font-medium">
                {wheyProtein.protein_per_serving}g
              </span>
            </div>
            <div className="flex justify-between">
              <span
                className={`${darkMode ? "text-gray-400" : "text-gray-600"}`}
              >
                Concentração:
              </span>
              <span className="font-medium">
                {wheyProtein.protein_concentration.toFixed(1)}%
              </span>
            </div>
          </div>
          <div
            className="inline-flex rounded-base shadow-xs -space-x-px"
            role="group"
          >
            <button
              type="button"
              className="text-body bg-neutral-primary-soft border border-default hover:bg-neutral-secondary-medium hover:text-heading focus:ring-3 focus:ring-neutral-tertiary-soft font-medium leading-5 rounded-s-base text-sm px-3 py-2 focus:outline-none"
            >
              Profile
            </button>
            <button
              type="button"
              className="text-body bg-neutral-primary-soft border border-default hover:bg-neutral-secondary-medium hover:text-heading focus:ring-3 focus:ring-neutral-tertiary-soft font-medium leading-5 text-sm px-3 py-2 focus:outline-none"
            >
              Settings
            </button>
            <button
              type="button"
              className="text-body bg-neutral-primary-soft border border-default hover:bg-neutral-secondary-medium hover:text-heading focus:ring-3 focus:ring-neutral-tertiary-soft font-medium leading-5 rounded-e-base text-sm px-3 py-2 focus:outline-none"
            >
              Messages
            </button>
          </div>
          <div className="flex flex-1 space-x-1">
            <button
              onClick={() => onEdit(wheyProtein)}
              className="flex-1 bg-yellow-600 hover:bg-yellow-700 text-white py-1 px-1 rounded text-xs"
            >
              Editar
            </button>
            <button
              onClick={() => onDelete(wheyProtein.id)}
              className="flex-1 bg-red-600 hover:bg-red-700 text-white py-1 px-1 rounded text-xs"
            >
              Excluir
            </button>
          </div>
        </div>
      </Card>
    </>
  );
};
