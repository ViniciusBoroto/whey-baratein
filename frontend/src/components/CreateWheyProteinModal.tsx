import { Modal } from "./Modal";
import { Input } from "./Input";
import type { WheyProteinCreate } from "../types/whey-protein";
import { useEffect, useMemo, useState } from "react";
import type { Brand } from "../types/whey-protein";
import { PrimaryButton } from "./PrimaryButton";
import { brandService } from "../services/brand.service";
import { wheyProteinService } from "../services/whey-protein.service";

export interface CreateModalFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export const CreateWheyProteinModal: React.FC<CreateModalFormProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const [whey, setWhey] = useState<WheyProteinCreate>({
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
  const [brand, setBrand] = useState({
    name: "",
    logo_url: "",
    description: "",
  });
  const [selectedBrand, setSelectedBrand] = useState<Brand | null>(null);
  const [brandQuery, setBrandQuery] = useState("");
  const [creatingBrand, setCreatingBrand] = useState(false);
  const [brands, setBrands] = useState<Brand[]>([]);

  useEffect(() => {
    const fetchBrands = async () => {
      try {
        const b = await brandService.getAll();
        setBrands(b);
      } catch (error) {
        console.error("Error loading brands:", error);
      }
    };
    fetchBrands();
  }, []);
  const filteredBrands = useMemo(() => {
    if (!brandQuery) return [];
    return brands.filter((item) =>
      item.name.toLowerCase().includes(brandQuery.toLowerCase()),
    );
  }, [brandQuery, brands]);

  const handleBrandSelect = (brand: Brand) => {
    setSelectedBrand(brand);
    setWhey((prev) => ({ ...prev, brand_id: brand.id }));
    setBrandQuery(brand.name);
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
      [id]: value === "" ? "" : Number(value) || value,
    }));
  };

  const handleSubmitBrand = async (e: React.MouseEvent) => {
    e.preventDefault();
    if (!brand.name) return;

    try {
      const newBrand = await brandService.create({
        name: brand.name,
        description: brand.description,
        logo_url: brand.logo_url,
      });
      setBrands((prev) => [...prev, newBrand]);
      setSelectedBrand(newBrand);
      setWhey((prev) => ({ ...prev, brand_id: newBrand.id }));
      setCreatingBrand(false);
      setBrandQuery(newBrand.name);
      setBrand({ name: "", logo_url: "", description: "" });
    } catch (error) {
      console.error("Error creating brand:", error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!whey.name || !whey.price || !whey.total_weight || !whey.serving_size || !whey.protein_per_serving || !selectedBrand) {
      alert("Preencha todos os campos obrigatórios");
      return;
    }

    try {
      await wheyProteinService.create(whey);
      onSuccess?.();
      onClose();
    } catch (error) {
      console.error("Error creating whey protein:", error);
      alert("Erro ao criar produto");
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Adicionar Whey Protein" closeOnOutsideClick={false}>
      <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-x-4">
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
          {!creatingBrand && selectedBrand && (
            <div className="flex items-center col-span-2 px-3">
              <p className="mr-3 text-sm text-heading">
                <strong>Selecionada: </strong>
              </p>
              <div className="flex items-center border-border-light border rounded-full shadow-md shadow-border-light px-2 py-0.5 bg-surface-strong">
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
            <ul className="col-span-2 p-0 m-0 mb-5 -mt-3 rounded-md border border-border-light overflow-hidden">
              {filteredBrands.map((brand) => (
                <li
                  className="group cursor-pointer flex items-center border-b border-border-light p-3 bg-surface-alt hover:bg-surface transition-colors duration-200"
                  key={brand.id}
                  onClick={() => handleBrandSelect(brand)}
                >
                  <img
                    src={brand.logo_url || "https://placehold.co/50x50"}
                    alt="Logo da marca"
                    className="rounded-full w-8 h-8 mr-3 object-cover shrink-0"
                  />
                  {brand.name}
                </li>
              ))}
              <li
                className="cursor-pointer text-brand p-3 hover:bg-brand-light hover:text-white transition-colors duration-200"
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
                type="button"
                className="col-span-1 bg-red-600 hover:bg-red-700"
                onClick={() => setCreatingBrand(false)}
              >
                Cancelar
              </PrimaryButton>
              <PrimaryButton type="button" className="col-span-1" onClick={handleSubmitBrand}>
                Criar
              </PrimaryButton>
            </form>
          )}
        </fieldset>
        <Input
          label="Preço (R$/pacote)"
          id="price"
          type="number"
          step="0.01"
          min="0"
          value={whey.price}
          onChange={handleInputChange}
          placeholder="0,00"
          required
        />
        <Input
          label="Tamanho (g/pacote)"
          id="total_weight"
          type="number"
          min="0"
          value={whey.total_weight}
          onChange={handleInputChange}
          placeholder="0"
          required
        />
        <Input
          label="URL da Imagem"
          id="image_url"
          type="text"
          value={whey.image_url}
          onChange={handleInputChange}
          placeholder="https://..."
          wrapperClassName="col-span-2"
        />

        <fieldset className="my-2 px-4 grid grid-cols-2 gap-x-2 border border-border-medium col-span-2 rounded-md">
          <legend className="grid grid-cols-2mb-2 p-3 text-sm font-semibold text-heading">
            Dose
          </legend>
          <Input
            label="Tamanho da dose (g)"
            id="serving_size"
            type="number"
            min="0"
            value={whey.serving_size}
            onChange={handleInputChange}
            placeholder="0"
            required
          />
          <Input
            label="Proteína por dose (g)"
            id="protein_per_serving"
            type="number"
            min="0"
            value={whey.protein_per_serving}
            onChange={handleInputChange}
            placeholder="0"
            required
          />
          <Input
            label="Confiabilidade (0-5)"
            id="reliability"
            type="number"
            min="0"
            max="5"
            value={whey.reliability}
            onChange={handleInputChange}
            placeholder="0"
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
            min="0"
            value={whey.fenilanina}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Histidina (mg)"
            id="histidina"
            type="number"
            min="0"
            value={whey.histidina}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Isoleucina (mg)"
            id="isoleucina"
            type="number"
            min="0"
            value={whey.isoleucina}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Leucina (mg)"
            id="leucina"
            type="number"
            min="0"
            value={whey.leucina}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Lisina (mg)"
            id="lisina"
            type="number"
            min="0"
            value={whey.lisina}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Metionina (mg)"
            id="metionina"
            type="number"
            min="0"
            value={whey.metionina}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Treonina (mg)"
            id="treonina"
            type="number"
            min="0"
            value={whey.treonina}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Triptofano (mg)"
            id="triptofano"
            type="number"
            min="0"
            value={whey.triptofano}
            onChange={handleInputChange}
            placeholder="000"
          />
          <Input
            label="Valina (mg)"
            id="valina"
            type="number"
            min="0"
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
