import { Modal } from "./Modal";
import { Input } from "./Input";
import type { WheyProtein } from "../types/whey-protein";
import { useEffect, useMemo, useState } from "react";
import type { Brand } from "../types/whey-protein";
import { PrimaryButton } from "./PrimaryButton";
import { brandService } from "../services/brand.service";

export interface CreateModalFormProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CreateWheyProteinModal: React.FC<CreateModalFormProps> = ({
  isOpen,
  onClose,
}) => {
  const [whey, setWhey] = useState<WheyProtein>({
    id: 0,
    name: "",
    eea_per_serving: 0,
    eea_price: 0,
    fenilanina: 0,
    histidina: 0,
    isoleucina: 0,
    leucina: 0,
    lisina: 0,
    metionina: 0,
    treonina: 0,
    price: 0,
    protein_concentration: 0,
    protein_per_serving: 0,
    reliability: 0,
    servings_per_packet: 0,
    total_eea_per_packet: 0,
    total_weight: 0,
    serving_size: 0,
    triptofano: 0,
    valina: 0,
    brand_id: undefined,
    image_url: undefined,
  });
  const [brand, setBrand] = useState<Brand>({
    id: 0,
    name: "",
    logo_url: "",
    description: "",
  });
  const [selectedBrand, setSelectedBrand] = useState<Brand>({
    id: 0,
    name: "",
    logo_url: "",
    description: "",
  });
  const [brandQuery, setBrandQuery] = useState("");
  const [creatingBrand, setCreatingBrand] = useState(false);
  const [brands, setBrands] = useState<Brand[]>([]);
  useEffect(() => {
    const fetch = async () => {
      try {
        let b = await brandService.getAll();
        setBrands(b);
      } catch (error) {
        console.error("Error loading brands:", error);
      }
    };
    fetch();
  });
  const filteredBrands = useMemo(() => {
    if (!brandQuery) return [];
    return brands.filter((item) =>
      item.name.toLowerCase().includes(brandQuery.toLowerCase()),
    );
  }, [brandQuery, brands]);

  const handleBrandSelect = (brand: Brand) => {
    setSelectedBrand(brand);
    setBrandQuery("");
    setCreatingBrand(false);
  };

  const handleBrandInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBrandQuery(e.target.value);
  };

  const handleNewBrandChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    const field = id.replace("brand_", "");
    setBrand((prev) => ({ ...prev, [field]: value }));
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    setWhey((prev) => ({
      ...prev,
      [id]: value === "" ? 0 : Number(value) || value,
    }));
  };

  const handleSubmitBrand = () => {
    try {
      brandService.create({
        name: brand.name,
        description: brand.description,
        logo_url: brand.logo_url,
      });
    } catch (error) {
      console.error("Error creating brand:", error);
      return;
    }

    setBrands((prev) => [...prev, brand]);
    setSelectedBrand(brand);
    setCreatingBrand(false);
    setBrandQuery("");
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Adicionar Whey Protein">
      <form action="#" className="grid grid-cols-2 gap-x-4">
        <Input
          label="Nome"
          id="name"
          type="text"
          value={whey.name}
          onChange={handleInputChange}
          placeholder="Nome do whey"
          wrapperClassName="col-span-2"
          required
        />

        <fieldset className="my-2 px-4 pb-5 mb-5 grid grid-cols-2 gap-x-2 border border-border-medium col-span-2 rounded-md">
          <legend className="grid grid-cols-2mb-2 p-3 text-sm font-semibold text-heading">
            Marca
          </legend>
          {/* SELECTED BRAND */}
          {!creatingBrand && selectedBrand.id != 0 && (
            <div className="flex items-center col-span-2 px-3">
              <p className="mr-3 text-sm text-heading">
                <strong>Selecionada: </strong>
              </p>
              <div className="flex items-center border-border-light border rounded-full shadow-md shadow-border-light px-2">
                <img
                  src={selectedBrand.logo_url || "https://placehold.co/50x50"}
                  alt="Logo da marca"
                  className="rounded-full w-8 my-1 mr-3 group-hover:scale-110 group-hover:shadow-md group-hover:shadow-brand shadow-border transition duration-300 ease-in-out"
                />
                <p>{selectedBrand.name}</p>
              </div>
            </div>
          )}
          {/* Brand input */}
          {!creatingBrand && (
            <Input
              label="Pesquisar marca"
              id="brand"
              type="text"
              value={brandQuery}
              onChange={handleBrandInputChange}
              placeholder="Nome da marca"
              wrapperClassName="col-span-2"
              required
            />
          )}
          {/* BRAND LIST */}
          {brandQuery && !creatingBrand && (
            <ul className="col-span-2 p-0 m-0 mb-5 -mt-3 rounded-base border-border">
              {filteredBrands.map((brand) => (
                <li
                  className="group flex items-center border border-border-light p-3 bg-surface-alt hover:bg-surface border-b-border hover:border-x-brand-light light hover:border-y-0 hover:border-x  "
                  key={brand.id}
                  onClick={() => handleBrandSelect(brand)}
                >
                  <img
                    src={brand.logo_url || "https://placehold.co/50x50"}
                    alt="Logo da marca"
                    className="rounded-full w-8 my-1 mr-3 group-hover:scale-110 group-hover:shadow-md group-hover:shadow-brand shadow-border transition duration-300 ease-in-out"
                  />
                  {brand.name}
                </li>
              ))}
              <li
                className="cursor-pointer text-brand border-b border-x border-brand-light p-3 hover:bg-brand-light hover:text-white  rounded-b-base"
                onClick={() => setCreatingBrand(true)}
              >
                + Adicionar Marca
              </li>
            </ul>
          )}
          {/* BRAND FORM */}
          {creatingBrand && (
            <form className="col-span-2 grid grid-cols-2 gap-x-2">
              <Input
                label="Nome da nova marca"
                id="brand_name"
                type="text"
                value={brand.name}
                onChange={handleNewBrandChange}
                placeholder="Digite o nome da marca"
                wrapperClassName="col-span-2"
                required
              />
              <Input
                label="Descrição"
                id="brand_description"
                type="text"
                value={brand.description}
                onChange={handleNewBrandChange}
                placeholder="Descrição da marca"
                wrapperClassName="col-span-2"
              />
              <Input
                label="URL do Logo"
                id="brand_logo_url"
                type="text"
                value={brand.logo_url}
                onChange={handleNewBrandChange}
                placeholder="https://..."
                wrapperClassName="col-span-2"
              />
              <PrimaryButton
                className="col-span-1 bg-red-600 hover:bg-red-700"
                onClick={() => setCreatingBrand(false)}
              >
                Cancelar
              </PrimaryButton>
              <PrimaryButton className="col-span-1" onClick={handleSubmitBrand}>
                Criar
              </PrimaryButton>
            </form>
          )}
        </fieldset>
        <Input
          label="Preço (R$/pacote)"
          id="price"
          type="number"
          value={whey.price}
          onChange={handleInputChange}
          placeholder="0,00"
          required
        />
        <Input
          label="Tamanho (g/pacote)"
          id="total_weight"
          type="number"
          value={whey.total_weight}
          onChange={handleInputChange}
          placeholder="0"
          required
        />

        <fieldset className="my-2 px-4 grid grid-cols-2 gap-x-2 border border-border-medium col-span-2 rounded-md">
          <legend className="grid grid-cols-2mb-2 p-3 text-sm font-semibold text-heading">
            Dose
          </legend>
          <Input
            label="Tamanho da dose (g)"
            id="serving_size"
            type="number"
            value={whey.serving_size}
            onChange={handleInputChange}
            placeholder="0"
            required
          />
          <Input
            label="Proteína por dose (g)"
            id="protein_per_serving"
            type="number"
            value={whey.protein_per_serving}
            onChange={handleInputChange}
            placeholder="0"
            required
          />
        </fieldset>
        <fieldset className="my-2 px-4 grid grid-cols-3 gap-x-2 border border-border-medium col-span-2 rounded-md">
          <legend className="mb-2 p-3 text-sm font-semibold text-heading">
            Aminograma
          </legend>
          <Input
            label="Fenilanina (mg)"
            id="fenilanina"
            type="number"
            value={whey.fenilanina}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Histidina (mg)"
            id="histidina"
            type="number"
            value={whey.histidina}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Isoleucina (mg)"
            id="isoleucina"
            type="number"
            value={whey.isoleucina}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Leucina (mg)"
            id="leucina"
            type="number"
            value={whey.leucina}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Lisina (mg)"
            id="lisina"
            type="number"
            value={whey.lisina}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Metionina (mg)"
            id="metionina"
            type="number"
            value={whey.metionina}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Treonina (mg)"
            id="treonina"
            type="number"
            value={whey.treonina}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Triptofano (mg)"
            id="triptofano"
            type="number"
            value={whey.triptofano}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Valina (mg)"
            id="valina"
            type="number"
            value={whey.valina}
            onChange={handleInputChange}
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
