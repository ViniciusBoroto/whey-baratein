import React from 'react';
import { WheyProteinRanking } from '../types/whey-protein';
import { Card, CardHeader, CardContent } from './Card';
import { formatPercentage, getRankColor, getRankIcon } from '../utils/formatters';

interface RankingCardProps {
  ranking: WheyProteinRanking;
  type: 'eea-price' | 'protein-concentration';
}

export const RankingCard: React.FC<RankingCardProps> = ({ ranking, type }) => {
  const isEeaPrice = type === 'eea-price';
  const primaryValue = isEeaPrice ? ranking.eea_price.toFixed(2) : formatPercentage(ranking.protein_concentration);
  const secondaryValue = isEeaPrice ? formatPercentage(ranking.protein_concentration) : ranking.eea_price.toFixed(2);
  const primaryLabel = isEeaPrice ? 'EAA/Preço' : 'Concentração';
  const secondaryLabel = isEeaPrice ? 'Concentração' : 'EAA/Preço';

  return (
    <Card>
      <CardHeader
        title={ranking.name}
        subtitle={ranking.brand}
        badge={
          <span className={`px-3 py-1 text-sm font-bold rounded-full ${getRankColor(ranking.rank)}`}>
            {getRankIcon(ranking.rank)}
          </span>
        }
      />
      <CardContent>
        <div className="flex justify-between items-center">
          <div className="text-center">
            <p className="text-2xl font-bold text-blue-600">{primaryValue}</p>
            <p className="text-xs text-gray-600">{primaryLabel}</p>
          </div>
          <div className="text-center">
            <p className="text-lg font-semibold text-gray-700">{secondaryValue}</p>
            <p className="text-xs text-gray-600">{secondaryLabel}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};