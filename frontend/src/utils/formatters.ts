export const formatCurrency = (value: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(value);
};

export const formatPercentage = (value: number): string => {
  return `${value.toFixed(1)}%`;
};

export const formatWeight = (value: number): string => {
  return `${value}g`;
};

export const getRankColor = (rank: number): string => {
  if (rank === 1) return 'text-yellow-600 bg-yellow-50';
  if (rank === 2) return 'text-gray-600 bg-gray-50';
  if (rank === 3) return 'text-amber-600 bg-amber-50';
  return 'text-blue-600 bg-blue-50';
};

export const getRankIcon = (rank: number): string => {
  if (rank === 1) return '🥇';
  if (rank === 2) return '🥈';
  if (rank === 3) return '🥉';
  return `#${rank}`;
};