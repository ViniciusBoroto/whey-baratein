import React, { useState, useEffect } from "react";
import "./App.css";
import { BrandSelector } from "./components/BrandSelector";

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

    const totalEaa = eeaValues.reduce((sum, val) => (sum || 0) + (val || 0), 0) || 0;
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
      const [proteinsRes, eeaRes, concRes] = await Promise.all([
        fetch("/whey-proteins/"),
        fetch("/whey-proteins/rankings/eea-price"),
        fetch("/whey-proteins/rankings/protein-concentration"),
      ]);

      setProteins(await proteinsRes.json());
      setEeaRanking(await eeaRes.json());
      setConcentrationRanking(await concRes.json());
    } catch (error) {
      console.error("Error loading data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const url = editingId ? `/whey-proteins/${editingId}` : "/whey-proteins/";
      const method = editingId ? "PUT" : "POST";

      await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

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
        await fetch(`/whey-proteins/${id}`, { method: "DELETE" });
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
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
            {proteins.map((protein) => (
              <div
                key={protein.id}
                className={`rounded-lg shadow-md p-4 ${
                  darkMode
                    ? "bg-gray-800 border-gray-700"
                    : "bg-white border-gray-200"
                } border`}
              >
                {protein.image_url && (
                  <img
                    src={protein.image_url}
                    alt={protein.name}
                    className="w-full h-32 object-cover rounded-lg mb-3"
                  />
                )}
                <div className="flex justify-between items-start mb-2">
                  <div className="flex-1">
                    <h3 className="text-sm font-semibold truncate">
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
                  <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full ml-2">
                    R$ {protein.price.toFixed(0)}
                  </span>
                </div>

                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-1">
                    {Array.from({ length: 5 }, (_, i) => (
                      <svg
                        key={i}
                        className={`w-3 h-3 ${
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
                  <span className="text-xs text-gray-500">
                    ({protein.reliability}/5)
                  </span>
                </div>

                <div className="space-y-1 mb-3 text-xs">
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
                  <div className="flex justify-between">
                    <span
                      className={`${
                        darkMode ? "text-gray-400" : "text-gray-600"
                      }`}
                    >
                      Preço/EAA:
                    </span>
                    <span className="font-medium text-green-600">
                      {protein.eea_price.toFixed(2)}
                    </span>
                  </div>
                </div>

                <div className="flex space-x-1">
                  <button
                    onClick={() => handleEdit(protein)}
                    className="flex-1 bg-yellow-600 hover:bg-yellow-700 text-white py-1 px-2 rounded text-xs"
                  >
                    Editar
                  </button>
                  <button
                    onClick={() => handleDelete(protein.id)}
                    className="flex-1 bg-red-600 hover:bg-red-700 text-white py-1 px-2 rounded text-xs"
                  >
                    Excluir
                  </button>
                </div>
              </div>
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
                  <label
                    className={`block text-sm font-medium mb-1 ${
                      darkMode ? "text-gray-300" : "text-gray-700"
                    }`}
                  >
                    Confiabilidade (0-5 estrelas)
                  </label>
                  <div className="flex items-center space-x-2">
                    <input
                      type="range"
                      min="0"
                      max="5"
                      value={formData.reliability}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          reliability: Number(e.target.value),
                        })
                      }
                      className="flex-1"
                    />
                    <div className="flex items-center space-x-1">
                      {Array.from({ length: 5 }, (_, i) => (
                        <svg
                          key={i}
                          className={`w-4 h-4 ${
                            i < (formData.reliability || 0)
                              ? "text-yellow-400"
                              : "text-gray-300"
                          }`}
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                      ))}
                      <span className="text-sm ml-2">
                        ({formData.reliability || 0}/5)
                      </span>
                    </div>
                  </div>
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
