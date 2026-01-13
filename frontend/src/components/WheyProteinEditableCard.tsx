import type { WheyProtein } from "../types/whey-protein";

interface WheyProteinEditableCardProps {
  wheyProtein: WheyProtein;
}

export const WheyProteinEditableCard =({protein}) => {
   return (
    <>
        key={protein.id}
        className={`rounded-lg shadow-sm p-3 ${
            darkMode
            ? "bg-gray-800 border-gray-700"
            : "bg-white border-gray-200"
        } border hover:shadow-md transition-shadow`}
        >
        {protein.image_url && (
            <img
            src={protein.image_url}
            alt={protein.name}
            className="w-full h-20 object-cover rounded mb-1"
            />
        )}
        <div className="mb-2">
            <h3 className="text-xs font-semibold truncate">
            {protein.name}
            </h3>
            <p
            className={`text-xs ${
                darkMode ? "text-gray-400" : "text-gray-600"
            }`}
            >
            {protein.brand?.name || "Sem marca"}
            </p>
        </div>

        <div className="flex items-center justify-between mb-2">
            <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded">
            R$ {protein.price.toFixed(0)}
            </span>
            <div className="flex items-center space-x-1">
            {Array.from({ length: 5 }, (_, i) => (
                <svg
                key={i}
                className={`w-2 h-2 ${
                    i < protein.reliability
                    ? "text-yellow-400"
                    : "text-gray-300"
                }`}
                fill="currentColor"
                viewBox="0 0 20 20"
                >
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
            ))}
            </div>
        </div>

        <div className="space-y-1 mb-2 text-xs">
            <div className="flex justify-between">
            <span
                className={`${
                darkMode ? "text-gray-400" : "text-gray-600"
                }`}
            >
                Proteína:
            </span>
            <span className="font-medium">
                {protein.protein_per_serving}g
            </span>
            </div>
            <div className="flex justify-between">
            <span
                className={`${
                darkMode ? "text-gray-400" : "text-gray-600"
                }`}
            >
                Concentração:
            </span>
            <span className="font-medium">
                {protein.protein_concentration.toFixed(1)}%
            </span>
            </div>
        </div>

        <div className="flex space-x-1">
            <button
            onClick={() => handleEdit(protein)}
            className="flex-1 bg-yellow-600 hover:bg-yellow-700 text-white py-1 px-1 rounded text-xs"
            >
            Editar
            </button>
            <button
            onClick={() => handleDelete(protein.id)}
            className="flex-1 bg-red-600 hover:bg-red-700 text-white py-1 px-1 rounded text-xs"
            >
            Excluir
            </button>
        </div>
    </>

   ) 
}