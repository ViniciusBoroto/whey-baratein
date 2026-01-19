import React, { useState, useEffect } from "react";
import "./App.css";
import { BrandSelector } from "./components/BrandSelector";
import { StarSlider } from "./components/StarSlider";
import { wheyProteinService } from "./services/whey-protein.service";
import { WheyProteinEditableCard } from "./components/WheyProteinEditableCard";
import type { WheyProteinCard } from "./components/WheyProteinCard";

interface WheyProtein {
  id: number;
  name: string;
  brand?: { name: string; id: number; logo_url?: string };
  brand_id?: number;
  price: number;
  serving_size: number;
  total_weight: number;
  protein_per_serving: number;
  reliability: number;
  image_url?: string;
  fenilanina: number;
  histidina: number;
  isoleucina: number;
  leucina: number;
  lisina: number;
  metionina: number;
  treonina: number;
  triptofano: number;
  valina: number;
  eea_per_serving: number;
  servings_per_packet: number;
  total_eea_per_packet: number;
  eea_price: number;
  protein_concentration: number;
}

interface WheyProteinCreate {
  name: string;
  price: number;
  brand_id?: number;
  serving_size: number;
  total_weight: number;
  protein_per_serving: number;
  reliability?: number;
  image_url?: string;
  fenilanina?: number;
  histidina?: number;
  isoleucina?: number;
  leucina?: number;
  lisina?: number;
  metionina?: number;
  treonina?: number;
  triptofano?: number;
  valina?: number;
}

interface Ranking {
  id: number;
  name: string;
  brand: string;
  eea_price: number;
  protein_concentration: number;
  rank: number;
}

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [activeTab, setActiveTab] = useState("products");
  const [proteins, setProteins] = useState<WheyProtein[]>([]);
  const [eeaRanking, setEeaRanking] = useState<Ranking[]>([]);
  const [concentrationRanking, setConcentrationRanking] = useState<Ranking[]>(
    []
  );
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [unitWarning, setUnitWarning] = useState<string | null>(null);
  const [formData, setFormData] = useState<WheyProteinCreate>({
    name: "",
    price: 0,
    brand_id: undefined,
    serving_size: 0,
    total_weight: 0,
    protein_per_serving: 0,
    reliability: 0,
    image_url: "",
    fenilanina: 0,
    histidina: 0,
    isoleucina: 0,
    leucina: 0,
    lisina: 0,
    metionina: 0,
    treonina: 0,
    triptofano: 0,
    valina: 0,
  });

  const checkEaaUnits = (data: WheyProteinCreate) => {
    const eeaValues = [
      data.fenilanina,
      data.histidina,
      data.isoleucina,
      data.leucina,
      data.lisina,
      data.metionina,
      data.treonina,
      data.triptofano,
      data.valina,
    ].filter((v) => v && v > 0);

    if (eeaValues.length === 0 || data.serving_size === 0) {
      setUnitWarning(null);
      return;
    }

    const totalEaa =
      eeaValues.reduce((sum, val) => (sum || 0) + (val || 0), 0) || 0;
    const avgEaa = eeaValues.length > 0 ? totalEaa / eeaValues.length : 0;

    if (avgEaa > data.serving_size * 10) {
      setUnitWarning(
        "Os valores de aminoácidos parecem estar em mg. O sistema converterá automaticamente para gramas."
      );
    } else {
      setUnitWarning(null);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [proteins, eeaRanking, concRanking] = await Promise.all([
        wheyProteinService.getAll(),
        wheyProteinService.getRanking("eea-price"),
        wheyProteinService.getRanking("protein-concentration"),
      ]);

      setProteins(proteins);
      setEeaRanking(eeaRanking);
      setConcentrationRanking(concRanking);
    } catch (error) {
      console.error("Error loading data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingId) {
        await wheyProteinService.update(editingId, formData);
      } else {
        await wheyProteinService.create(formData);
      }

      setShowForm(false);
      setEditingId(null);
      resetForm();
      loadData();
    } catch (error) {
      console.error("Error saving:", error);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm("Tem certeza que deseja excluir?")) {
      try {
        await wheyProteinService.delete(id);
        loadData();
      } catch (error) {
        console.error("Error deleting:", error);
      }
    }
  };

  const handleEdit = (protein: WheyProtein) => {
    setFormData({
      name: protein.name,
      price: protein.price,
      brand_id: protein.brand_id,
      serving_size: protein.serving_size,
      total_weight: protein.total_weight,
      protein_per_serving: protein.protein_per_serving,
      reliability: protein.reliability,
      image_url: protein.image_url || "",
      fenilanina: protein.fenilanina,
      histidina: protein.histidina,
      isoleucina: protein.isoleucina,
      leucina: protein.leucina,
      lisina: protein.lisina,
      metionina: protein.metionina,
      treonina: protein.treonina,
      triptofano: protein.triptofano,
      valina: protein.valina,
    });
    setEditingId(protein.id);
    setShowForm(true);
  };

  const resetForm = () => {
    setFormData({
      name: "",
      price: 0,
      brand_id: undefined,
      serving_size: 0,
      total_weight: 0,
      protein_per_serving: 0,
      reliability: 0,
      image_url: "",
      fenilanina: 0,
      histidina: 0,
      isoleucina: 0,
      leucina: 0,
      lisina: 0,
      metionina: 0,
      treonina: 0,
      triptofano: 0,
      valina: 0,
    });
    setUnitWarning(null);
  };

  if (loading) {
    return (
      <div
        className={`min-h-screen flex items-center justify-center ${
          darkMode ? "bg-gray-900" : "bg-gray-50"
        }`}
      >
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p className={darkMode ? "text-gray-300" : "text-gray-600"}>
            Carregando...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`min-h-screen ${
        darkMode ? "bg-gray-900 text-white" : "bg-gray-50 text-gray-900"
      }`}
    >
      {/* Header */}
      <div
        className={`${
          darkMode ? "bg-gray-800 border-gray-700" : "bg-white border-gray-200"
        } border-b`}
      >
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold">🥛 Whey Protein Manager</h1>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setDarkMode(!darkMode)}
                className={`p-2 rounded-lg ${
                  darkMode
                    ? "bg-gray-700 hover:bg-gray-600"
                    : "bg-gray-100 hover:bg-gray-200"
                }`}
              >
                {darkMode ? "☀️" : "🌙"}
              </button>
              <button
                onClick={() => {
                  setShowForm(true);
                  setEditingId(null);
                  resetForm();
                }}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium"
              >
                + Adicionar
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="flex space-x-1 mb-6">
          {[
            { id: "products", label: "Produtos", icon: "🥛" },
            {
              id: "eea-ranking",
              label: "Ranking custo-benefício",
              icon: "💰",
            },
            {
              id: "concentration-ranking",
              label: "Ranking Concentração",
              icon: "💪",
            },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                activeTab === tab.id
                  ? "bg-blue-600 text-white"
                  : darkMode
                  ? "bg-gray-800 text-gray-300 hover:bg-gray-700"
                  : "bg-white text-gray-600 hover:bg-gray-100"
              }`}
            >
              {tab.icon} {tab.label}
            </button>
          ))}
        </div>

        {/* Content */}
        {activeTab === "products" && (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3">
            {proteins.map((protein) => (
              <WheyProteinEditableCard
                key={protein.id}
                wheyProtein={protein}
                darkMode={darkMode}
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}

        {activeTab === "eea-ranking" && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-center mb-6">
              Ranking por custo-benefício
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {eeaRanking.map((item) => (
                <div
                  key={item.id}
                  className={`rounded-lg shadow-md p-6 ${
                    darkMode ? "bg-gray-800" : "bg-white"
                  }`}
                >
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="font-semibold">{item.name}</h3>
                      <p
                        className={`text-sm ${
                          darkMode ? "text-gray-400" : "text-gray-600"
                        }`}
                      >
                        {item.brand}
                      </p>
                    </div>
                    <span
                      className={`px-3 py-1 text-sm font-bold rounded-full ${
                        item.rank === 1
                          ? "bg-yellow-100 text-yellow-800"
                          : item.rank === 2
                          ? "bg-gray-100 text-gray-800"
                          : item.rank === 3
                          ? "bg-orange-100 text-orange-800"
                          : "bg-blue-100 text-blue-800"
                      }`}
                    >
                      #{item.rank}
                    </span>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-blue-600">
                      {item.eea_price.toFixed(2)}
                    </p>
                    <p
                      className={`text-xs ${
                        darkMode ? "text-gray-400" : "text-gray-600"
                      }`}
                    >
                      EAA/R$
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === "concentration-ranking" && (
          <div className="space-y-4">
            <h2 className="text-2xl font-bold text-center mb-6">
              Ranking por Concentração
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {concentrationRanking.map((item) => (
                <div
                  key={item.id}
                  className={`rounded-lg shadow-md p-6 ${
                    darkMode ? "bg-gray-800" : "bg-white"
                  }`}
                >
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="font-semibold">{item.name}</h3>
                      <p
                        className={`text-sm ${
                          darkMode ? "text-gray-400" : "text-gray-600"
                        }`}
                      >
                        {item.brand}
                      </p>
                    </div>
                    <span
                      className={`px-3 py-1 text-sm font-bold rounded-full ${
                        item.rank === 1
                          ? "bg-yellow-100 text-yellow-800"
                          : item.rank === 2
                          ? "bg-gray-100 text-gray-800"
                          : item.rank === 3
                          ? "bg-orange-100 text-orange-800"
                          : "bg-blue-100 text-blue-800"
                      }`}
                    >
                      #{item.rank}
                    </span>
                  </div>
                  <div className="text-center">
                    <p className="text-2xl font-bold text-green-600">
                      {item.protein_concentration.toFixed(1)}%
                    </p>
                    <p
                      className={`text-xs ${
                        darkMode ? "text-gray-400" : "text-gray-600"
                      }`}
                    >
                      Concentração
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Modal Form */}
      {showForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div
            className={`rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto ${
              darkMode ? "bg-gray-800" : "bg-white"
            }`}
          >
            <h2 className="text-xl font-bold mb-4">
              {editingId ? "Editar" : "Adicionar"} Produto
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label
                    className={`block text-sm font-medium mb-1 ${
                      darkMode ? "text-gray-300" : "text-gray-700"
                    }`}
                  >
                    Nome *
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={(e) =>
                      setFormData({ ...formData, name: e.target.value })
                    }
                    className={`w-full p-3 border rounded-lg ${
                      darkMode
                        ? "bg-gray-700 border-gray-600 text-white"
                        : "bg-white border-gray-300"
                    }`}
                    required
                  />
                </div>
                <div>
                  <BrandSelector
                    selectedBrandId={formData.brand_id}
                    onBrandSelect={(brandId) =>
                      setFormData({ ...formData, brand_id: brandId })
                    }
                    darkMode={darkMode}
                  />
                </div>
                <div>
                  <label
                    className={`block text-sm font-medium mb-1 ${
                      darkMode ? "text-gray-300" : "text-gray-700"
                    }`}
                  >
                    Preço (R$) *
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={formData.price}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        price: Number(e.target.value),
                      })
                    }
                    className={`w-full p-3 border rounded-lg ${
                      darkMode
                        ? "bg-gray-700 border-gray-600 text-white"
                        : "bg-white border-gray-300"
                    }`}
                    required
                  />
                </div>
                <div>
                  <label
                    className={`block text-sm font-medium mb-1 ${
                      darkMode ? "text-gray-300" : "text-gray-700"
                    }`}
                  >
                    Tamanho da Porção (g) *
                  </label>
                  <input
                    type="number"
                    value={formData.serving_size}
                    onChange={(e) => {
                      const newFormData = {
                        ...formData,
                        serving_size: Number(e.target.value),
                      };
                      setFormData(newFormData);
                      checkEaaUnits(newFormData);
                    }}
                    className={`w-full p-3 border rounded-lg ${
                      darkMode
                        ? "bg-gray-700 border-gray-600 text-white"
                        : "bg-white border-gray-300"
                    }`}
                    required
                  />
                </div>
                <div>
                  <label
                    className={`block text-sm font-medium mb-1 ${
                      darkMode ? "text-gray-300" : "text-gray-700"
                    }`}
                  >
                    Peso Total (g) *
                  </label>
                  <input
                    type="number"
                    value={formData.total_weight}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        total_weight: Number(e.target.value),
                      })
                    }
                    className={`w-full p-3 border rounded-lg ${
                      darkMode
                        ? "bg-gray-700 border-gray-600 text-white"
                        : "bg-white border-gray-300"
                    }`}
                    required
                  />
                </div>
                <div>
                  <label
                    className={`block text-sm font-medium mb-1 ${
                      darkMode ? "text-gray-300" : "text-gray-700"
                    }`}
                  >
                    Proteína por Porção (g) *
                  </label>
                  <input
                    type="number"
                    value={formData.protein_per_serving}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        protein_per_serving: Number(e.target.value),
                      })
                    }
                    className={`w-full p-3 border rounded-lg ${
                      darkMode
                        ? "bg-gray-700 border-gray-600 text-white"
                        : "bg-white border-gray-300"
                    }`}
                    required
                  />
                </div>
                <div>
                  <StarSlider
                    value={formData.reliability || 0}
                    onChange={(value) =>
                      setFormData({ ...formData, reliability: value })
                    }
                    darkMode={darkMode}
                  />
                </div>
              </div>

              <div>
                <label
                  className={`block text-sm font-medium mb-1 ${
                    darkMode ? "text-gray-300" : "text-gray-700"
                  }`}
                >
                  URL da Imagem
                </label>
                <input
                  type="url"
                  value={formData.image_url}
                  onChange={(e) =>
                    setFormData({ ...formData, image_url: e.target.value })
                  }
                  placeholder="https://exemplo.com/imagem.jpg"
                  className={`w-full p-3 border rounded-lg ${
                    darkMode
                      ? "bg-gray-700 border-gray-600 text-white"
                      : "bg-white border-gray-300"
                  }`}
                />
              </div>

              <h3
                className={`font-semibold mt-6 mb-3 ${
                  darkMode ? "text-gray-200" : "text-gray-800"
                }`}
              >
                Aminoácidos Essenciais (g ou mg)
              </h3>
              {unitWarning && (
                <div className="mb-4 p-3 bg-yellow-100 border border-yellow-400 text-yellow-700 rounded-lg text-sm">
                  ⚠️ {unitWarning}
                </div>
              )}
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {[
                  { key: "fenilanina", label: "Fenilalanina" },
                  { key: "histidina", label: "Histidina" },
                  { key: "isoleucina", label: "Isoleucina" },
                  { key: "leucina", label: "Leucina" },
                  { key: "lisina", label: "Lisina" },
                  { key: "metionina", label: "Metionina" },
                  { key: "treonina", label: "Treonina" },
                  { key: "triptofano", label: "Triptofano" },
                  { key: "valina", label: "Valina" },
                ].map((amino) => (
                  <div key={amino.key}>
                    <label
                      className={`block text-sm font-medium mb-1 ${
                        darkMode ? "text-gray-300" : "text-gray-700"
                      }`}
                    >
                      {amino.label}
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      value={
                        formData[amino.key as keyof WheyProteinCreate] || 0
                      }
                      onChange={(e) => {
                        const newFormData = {
                          ...formData,
                          [amino.key]: Number(e.target.value),
                        };
                        setFormData(newFormData);
                        checkEaaUnits(newFormData);
                      }}
                      className={`w-full p-3 border rounded-lg ${
                        darkMode
                          ? "bg-gray-700 border-gray-600 text-white"
                          : "bg-white border-gray-300"
                      }`}
                    />
                  </div>
                ))}
              </div>

              <div className="flex space-x-4 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg font-medium"
                >
                  {editingId ? "Atualizar" : "Salvar"}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false);
                    setEditingId(null);
                    resetForm();
                  }}
                  className={`flex-1 py-3 px-4 rounded-lg font-medium ${
                    darkMode
                      ? "bg-gray-700 hover:bg-gray-600 text-white"
                      : "bg-gray-200 hover:bg-gray-300 text-gray-800"
                  }`}
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
