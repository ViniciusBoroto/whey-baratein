export interface WheyProtein {
  id: number;
  name: string;
  price: number;
  brand?: Brand;
  brand_id?: number;
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

export interface WheyProteinCreate {
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

export interface WheyProteinRanking {
  id: number;
  name: string;
  brand: string;
  eea_price: number;
  protein_concentration: number;
  rank: number;
}

export type RankingType = "eea-price" | "protein-concentration";
export interface Brand {
  id: number;
  name: string;
  logo_url?: string;
  description?: string;
}

export interface BrandCreate {
  name: string;
  logo_url?: string;
  description?: string;
}
