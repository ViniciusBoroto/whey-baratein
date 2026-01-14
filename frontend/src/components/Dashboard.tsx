import React, { useState } from "react";
import type { WheyProteinRepository } from "../services/whey-protein.service";
import {
  useWheyProteins,
  useWheyProteinRanking,
} from "../hooks/useWheyProtein";
import { WheyProteinCard } from "./WheyProteinCard";
import { RankingCard } from "./RankingCard";
import { TabNavigation } from "./TabNavigation";
import { LoadingSpinner } from "./LoadingSpinner";

interface DashboardProps {
  wheyProteinRepository: WheyProteinRepository;
}

export const Dashboard: React.FC<DashboardProps> = ({
  wheyProteinRepository,
}) => {
  const [activeTab, setActiveTab] = useState("all");

  const {
    data: wheyProteins,
    loading: proteinsLoading,
    error: proteinsError,
  } = useWheyProteins(wheyProteinRepository);
  const {
    data: eeaRanking,
    loading: eeaLoading,
    error: eeaError,
  } = useWheyProteinRanking(wheyProteinRepository, "eea-price");
  const {
    data: concentrationRanking,
    loading: concentrationLoading,
    error: concentrationError,
  } = useWheyProteinRanking(wheyProteinRepository, "protein-concentration");

  const tabs = [
    { id: "all", label: "Todos os Produtos", icon: "🥛" },
    { id: "eea-ranking", label: "Ranking EAA/Preço", icon: "💰" },
    { id: "concentration-ranking", label: "Ranking Concentração", icon: "💪" },
  ];

  const renderContent = () => {
    if (activeTab === "all") {
      if (proteinsLoading)
        return <LoadingSpinner size="lg" className="py-12" />;
      if (proteinsError)
        return (
          <div className="text-red-600 text-center py-12">
            Erro: {proteinsError}
          </div>
        );
      if (!wheyProteins?.length)
        return (
          <div className="text-gray-600 text-center py-12">
            Nenhum produto encontrado
          </div>
        );

      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {wheyProteins.map((protein) => (
            <WheyProteinCard key={protein.id} wheyProtein={protein} />
          ))}
        </div>
      );
    }

    if (activeTab === "eea-ranking") {
      if (eeaLoading) return <LoadingSpinner size="lg" className="py-12" />;
      if (eeaError)
        return (
          <div className="text-red-600 text-center py-12">Erro: {eeaError}</div>
        );
      if (!eeaRanking?.length)
        return (
          <div className="text-gray-600 text-center py-12">
            Nenhum ranking encontrado
          </div>
        );

      return (
        <div className="space-y-4">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              Ranking por EAA/Preço
            </h2>
            <p className="text-gray-600 mt-2">
              Produtos ordenados pela melhor relação aminoácidos essenciais por
              preço
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {eeaRanking.map((ranking) => (
              <RankingCard
                key={ranking.id}
                ranking={ranking}
                type="eea-price"
              />
            ))}
          </div>
        </div>
      );
    }

    if (activeTab === "concentration-ranking") {
      if (concentrationLoading)
        return <LoadingSpinner size="lg" className="py-12" />;
      if (concentrationError)
        return (
          <div className="text-red-600 text-center py-12">
            Erro: {concentrationError}
          </div>
        );
      if (!concentrationRanking?.length)
        return (
          <div className="text-gray-600 text-center py-12">
            Nenhum ranking encontrado
          </div>
        );

      return (
        <div className="space-y-4">
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              Ranking por Concentração de Proteína
            </h2>
            <p className="text-gray-600 mt-2">
              Produtos ordenados pela maior concentração de proteína por porção
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {concentrationRanking.map((ranking) => (
              <RankingCard
                key={ranking.id}
                ranking={ranking}
                type="protein-concentration"
              />
            ))}
          </div>
        </div>
      );
    }

    return null;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Whey Protein Ranking
          </h1>
          <p className="text-xl text-gray-600">
            Compare e encontre o melhor whey protein para você
          </p>
        </div>

        <TabNavigation
          tabs={tabs}
          activeTab={activeTab}
          onTabChange={setActiveTab}
        />

        {renderContent()}
      </div>
    </div>
  );
};
