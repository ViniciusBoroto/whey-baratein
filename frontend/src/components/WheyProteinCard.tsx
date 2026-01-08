import React from 'react';
import { WheyProtein } from '../types/whey-protein';
import { Card, CardHeader, CardContent } from './Card';
import { formatCurrency, formatPercentage, formatWeight } from '../utils/formatters';

interface WheyProteinCardProps {
  wheyProtein: WheyProtein;
  onClick?: () => void;
}

export const WheyProteinCard: React.FC<WheyProteinCardProps> = ({ wheyProtein, onClick }) => {
  return (
    <Card onClick={onClick}>
      <CardHeader
        title={wheyProtein.name}
        subtitle={wheyProtein.brand}
        badge={
          <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
            {formatCurrency(wheyProtein.price)}
          </span>
        }
      />
      <CardContent>
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Proteína:</span>
              <span className="text-sm font-medium">{formatWeight(wheyProtein.protein_per_serving)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Concentração:</span>
              <span className="text-sm font-medium">{formatPercentage(wheyProtein.protein_concentration)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">EAA/Porção:</span>
              <span className="text-sm font-medium">{wheyProtein.eea_per_serving.toFixed(1)}g</span>
            </div>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Peso Total:</span>
              <span className="text-sm font-medium">{formatWeight(wheyProtein.total_weight)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Porções:</span>
              <span className="text-sm font-medium">{wheyProtein.servings_per_packet.toFixed(0)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">EAA/Preço:</span>
              <span className="text-sm font-medium text-green-600">{wheyProtein.eea_price.toFixed(2)}</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};