export const PrimaryButton = ({
  children,
  onClick,
}: {
  children: React.ReactNode;
  onClick?: () => void;
}) => {
  return (
    <button
      onClick={onClick}
      className="bg-brand hover:bg-brand-hover text-white font-bold py-2 px-4 rounded-base transition duration-180 hover:scale-103 hover:shadow-lg hover:-translate-y-1 hover:shadow-border"
    >
      {children}
    </button>
  );
};
