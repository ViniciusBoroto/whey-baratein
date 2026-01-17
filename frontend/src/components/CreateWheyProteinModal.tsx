import { Modal } from "./Modal";
import { Input } from "./Input";
import { useMemo, useState } from "react";
import type { Brand } from "../types/whey-protein";

export interface CreateModalFormProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CreateWheyProteinModal: React.FC<CreateModalFormProps> = ({
  isOpen,
  onClose,
}) => {
  const [brandQuery, setBrandQuery] = useState("");
  const brands: Brand[] = [
    { id: 1, name: "Optimum Nutrition" },
    { id: 2, name: "Gold Standard" },
  ];
  const filteredBrands = useMemo(() => {
    if (!brandQuery) return [];
    return brands.filter((item) =>
      item.name.toLowerCase().includes(brandQuery.toLowerCase()),
    );
  }, [brandQuery, brands]);

  const handleBrandInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBrandQuery(e.target.value);
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Adicionar Whey Protein">
      <form action="#" className="grid grid-cols-2 gap-x-4">
        <Input
          label="Nome"
          id="name"
          type="text"
          placeholder="Nome do whey"
          wrapperClassName="col-span-2"
          required
        />
        <div className="flex flex-col col-span-2 gap-0">
          <Input
            label="Marca"
            id="brand"
            type="text"
            value={brandQuery}
            onChange={handleBrandInputChange}
            placeholder="Marca do whey"
            wrapperClassName="col-span-2"
            required
          />
          {brandQuery && (
            <ul className="col-span-2 p-0 m-0 mb-5 -mt-4.5 rounded-b-base border-x border-b border-border">
              {filteredBrands.map((brand) => (
                <li
                  className="border border-border-light p-3 bg-surface-alt hover:bg-surface border-b-border"
                  key={brand.id}
                >
                  {brand.name}
                </li>
              ))}
              <li className="border text-brand border-border-light p-3 bg-surface-alt hover:bg-surface rounded-b-base">
                + Adicionar Marca
              </li>
            </ul>
          )}
        </div>
        <Input
          label="Preço (R$/pacote)"
          id="price"
          type="number"
          placeholder="0,00"
          required
        />
        <Input
          label="Tamanho (g/pacote)"
          id="quantity"
          type="number"
          placeholder="0"
          required
        />

        <fieldset className="my-2 px-4 grid grid-cols-2 gap-x-2 border border-border-medium col-span-2">
          <legend className="grid grid-cols-2mb-2 p-3 text-sm font-semibold text-heading">
            Dose
          </legend>
          <Input
            label="Tamanho da dose (g)"
            id="servingSize"
            type="number"
            placeholder="0"
            required
          />
          <Input
            label="Proteína por dose (g)"
            id="servingSize"
            type="number"
            placeholder="0"
            required
          />
        </fieldset>
        <fieldset className="my-2 px-4 grid grid-cols-3 gap-x-2 border border-border-medium col-span-2">
          <legend className="mb-2 p-3 text-sm font-semibold text-heading">
            Aminograma
          </legend>
          <Input
            label="Fenilanina (mg)"
            id="fenilanina"
            type="number"
            placeholder="000"
          />
          <Input
            label="Histidina (mg)"
            id="histidina"
            type="number"
            placeholder="000"
          />
          <Input
            label="Isoleucina (mg)"
            id="isoleucina"
            type="number"
            placeholder="000"
          />
          <Input
            label="Leucina (mg)"
            id="leucina"
            type="number"
            placeholder="000"
          />
          <Input
            label="Lisina (mg)"
            id="lisina"
            type="number"
            placeholder="000"
          />
          <Input
            label="Metionina (mg)"
            id="metionina"
            type="number"
            placeholder="000"
          />
          <Input
            label="Treonina (mg)"
            id="treonina"
            type="number"
            placeholder="000"
          />
          <Input
            label="Triptofano (mg)"
            id="triptofano"
            type="number"
            placeholder="000"
          />
          <Input
            label="Valina (mg)"
            id="valina"
            type="number"
            placeholder="000"
          />
        </fieldset>
        <button
          type="submit"
          className="col-span-2 text-white bg-brand box-border border border-transparent hover:bg-brand-strong focus:ring-4 focus:ring-brand-medium shadow-xs font-medium leading-5 rounded-base text-sm px-4 py-2.5 focus:outline-none w-full"
        >
          Adicionar
        </button>
      </form>
    </Modal>
  );
};
