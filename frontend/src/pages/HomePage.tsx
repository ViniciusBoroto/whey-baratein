import { useEffect, useState } from "react";
import { WheyCard } from "../components/WheyCard";
import type { WheyProtein } from "../types/whey-protein";
import { wheyProteinService } from "../services/whey-protein.service";

export const HomePage = () => {
  const wheyService = wheyProteinService;
  const [wheys, setWheys] = useState<WheyProtein[]>();

  useEffect(() => {
    wheyService.getAll().then(setWheys);
  }, []);

  return (
    <div className="grid sm:grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-7">
      {wheys?.map((whey) => (
        <WheyCard key={whey.id} whey={whey} />
      ))}
      {wheys?.map((whey) => (
        <WheyCard key={whey.id} whey={whey} />
      ))}
      {wheys?.map((whey) => (
        <WheyCard key={whey.id} whey={whey} />
      ))}
      {wheys?.map((whey) => (
        <WheyCard key={whey.id} whey={whey} />
      ))}
      {wheys?.map((whey) => (
        <WheyCard key={whey.id} whey={whey} />
      ))}
      {wheys?.map((whey) => (
        <WheyCard key={whey.id} whey={whey} />
      ))}
    </div>
  );
};
