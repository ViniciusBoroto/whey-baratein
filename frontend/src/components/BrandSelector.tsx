import React, { useState, useEffect } from "react";
import { brandService } from "../services/brand.service";

interface Brand {
  id: number;
  name: string;
  logo_url?: string;
  description?: string;
}

interface BrandCreate {
  name: string;
  logo_url?: string;
  description?: string;
}

interface BrandSelectorProps {
  selectedBrandId?: number;
  onBrandSelect: (brandId: number | undefined) => void;
  darkMode?: boolean;
}

export const BrandSelector: React.FC<BrandSelectorProps> = ({
  selectedBrandId,
  onBrandSelect,
  darkMode = false,
}) => {
  const [brands, setBrands] = useState<Brand[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newBrand, setNewBrand] = useState<BrandCreate>({
    name: "",
    logo_url: "",
    description: "",
  });

  useEffect(() => {
    loadBrands();
  }, []);

  const loadBrands = async () => {
    try {
      const data = await brandService.getAll();
      setBrands(data);
    } catch (error) {
      console.error("Error loading brands:", error);
    }
  };

  const createBrand = async () => {
    try {
      const createdBrand = await brandService.create(newBrand);
      setBrands([...brands, createdBrand]);
      onBrandSelect(createdBrand.id);
      setShowCreateForm(false);
      setNewBrand({ name: "", logo_url: "", description: "" });
      setSearchTerm("");
    } catch (error) {
      console.error("Error creating brand:", error);
    }
  };

  const filteredBrands = brands.filter((brand) =>
    brand.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const selectedBrand = brands.find((b) => b.id === selectedBrandId);

  return (
    <div className="space-y-2">
      <label
        className={`block text-sm font-medium ${
          darkMode ? "text-gray-300" : "text-gray-700"
        }`}
      >
        Marca
      </label>

      {/* Search/Select Input */}
      <div className="relative">
        <input
          type="text"
          value={selectedBrand ? selectedBrand.name : searchTerm}
          onChange={(e) => {
            setSearchTerm(e.target.value);
            if (selectedBrand && e.target.value !== selectedBrand.name) {
              onBrandSelect(undefined);
            }
          }}
          placeholder="Digite para buscar ou criar nova marca..."
          className={`w-full p-3 border rounded-lg ${
            darkMode
              ? "bg-gray-700 border-gray-600 text-white"
              : "bg-white border-gray-300"
          }`}
        />

        {/* Dropdown */}
        {searchTerm && !selectedBrand && (
          <div
            className={`absolute z-10 w-full mt-1 border rounded-lg shadow-lg ${
              darkMode
                ? "bg-gray-700 border-gray-600"
                : "bg-white border-gray-300"
            }`}
          >
            {filteredBrands.length > 0 ? (
              filteredBrands.map((brand) => (
                <div
                  key={brand.id}
                  onClick={() => {
                    onBrandSelect(brand.id);
                    setSearchTerm("");
                  }}
                  className={`p-3 cursor-pointer hover:bg-gray-100 ${
                    darkMode ? "hover:bg-gray-600" : "hover:bg-gray-100"
                  } flex items-center space-x-3`}
                >
                  {brand.logo_url && (
                    <img
                      src={brand.logo_url}
                      alt={brand.name}
                      className="w-6 h-6 object-contain"
                    />
                  )}
                  <div>
                    <div className="font-medium">{brand.name}</div>
                    {brand.description && (
                      <div
                        className={`text-xs ${
                          darkMode ? "text-gray-400" : "text-gray-500"
                        }`}
                      >
                        {brand.description}
                      </div>
                    )}
                  </div>
                </div>
              ))
            ) : (
              <div
                onClick={() => {
                  setNewBrand({ ...newBrand, name: searchTerm });
                  setShowCreateForm(true);
                }}
                className={`p-3 cursor-pointer hover:bg-gray-100 ${
                  darkMode ? "hover:bg-gray-600" : "hover:bg-gray-100"
                } text-blue-600`}
              >
                + Criar marca "{searchTerm}"
              </div>
            )}
          </div>
        )}
      </div>

      {/* Create Brand Form */}
      {showCreateForm && (
        <div
          className={`p-4 border rounded-lg ${
            darkMode
              ? "bg-gray-800 border-gray-600"
              : "bg-gray-50 border-gray-300"
          }`}
        >
          <h4 className="font-medium mb-3">Nova Marca</h4>
          <div className="space-y-3">
            <input
              type="text"
              placeholder="Nome da marca"
              value={newBrand.name}
              onChange={(e) =>
                setNewBrand({ ...newBrand, name: e.target.value })
              }
              className={`w-full p-2 border rounded ${
                darkMode
                  ? "bg-gray-700 border-gray-600 text-white"
                  : "bg-white border-gray-300"
              }`}
            />
            <input
              type="url"
              placeholder="URL do logo (opcional)"
              value={newBrand.logo_url}
              onChange={(e) =>
                setNewBrand({ ...newBrand, logo_url: e.target.value })
              }
              className={`w-full p-2 border rounded ${
                darkMode
                  ? "bg-gray-700 border-gray-600 text-white"
                  : "bg-white border-gray-300"
              }`}
            />
            <textarea
              placeholder="Descrição (opcional)"
              value={newBrand.description}
              onChange={(e) =>
                setNewBrand({ ...newBrand, description: e.target.value })
              }
              className={`w-full p-2 border rounded ${
                darkMode
                  ? "bg-gray-700 border-gray-600 text-white"
                  : "bg-white border-gray-300"
              }`}
              rows={2}
            />
            <div className="flex space-x-2">
              <button
                onClick={createBrand}
                disabled={!newBrand.name}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
              >
                Criar
              </button>
              <button
                onClick={() => {
                  setShowCreateForm(false);
                  setNewBrand({ name: "", logo_url: "", description: "" });
                }}
                className={`px-4 py-2 rounded ${
                  darkMode
                    ? "bg-gray-600 hover:bg-gray-500"
                    : "bg-gray-300 hover:bg-gray-400"
                }`}
              >
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
