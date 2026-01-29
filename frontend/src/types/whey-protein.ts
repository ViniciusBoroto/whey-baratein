export interface WheyProtein {
  id: number;
  name: string;
  price: number;
  brand?: Brand;
  brand_id?: number;
  owner_id?: number;
  serving_size: number;
  total_weight: number;
  protein_per_serving: number;
  image_url?: string;
  phenylalanine_mg?: number;
  histidine_mg?: number;
  isoleucine_mg?: number;
  leucine_mg?: number;
  lysine_mg?: number;
  methionine_mg?: number;
  threonine_mg?: number;
  tryptophan_mg?: number;
  valine_mg?: number;
  servings_per_packet: number;
  protein_concentration_pct: number;
  eaa_price_per_g?: number;
}

export interface WheyProteinCreate {
  name: string;
  price: number;
  brand_id?: number;
  owner_id?: number;
  serving_size: number;
  total_weight: number;
  protein_per_serving: number;
  image_url?: string;
  phenylalanine_mg?: number;
  histidine_mg?: number;
  isoleucine_mg?: number;
  leucine_mg?: number;
  lysine_mg?: number;
  methionine_mg?: number;
  threonine_mg?: number;
  tryptophan_mg?: number;
  valine_mg?: number;
}

export interface WheyProteinRanking {
  id: number;
  name: string;
  brand: string;
  eea_price: number;
  protein_concentration: number;
  rank: number;
}

export type RankingType = "eea-price" | "protein-concentration";
export interface User {
  id: number;
  name: string;
  email: string;
  role: "user" | "admin";
}

export interface Brand {
  id: number;
  name: string;
  logo_url?: string;
  description?: string;
  owner_id?: number;
  owner?: User;
}

export interface BrandCreate {
  name: string;
  logo_url?: string;
  description?: string;
  owner_id?: number;
}
