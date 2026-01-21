export const PrimaryButton = ({
  children,
  onClick,
  className = "",
}: {
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
}) => {
  const baseClasses =
    "bg-brand hover:bg-brand-hover text-white font-bold py-2 px-4 rounded-base transition duration-180 hover:scale-103 hover:shadow-lg hover:-translate-y-1 hover:shadow-border";
  const composedClasses = `${baseClasses} ${className || ""}`.trim();

  return (
    <button onClick={onClick} className={composedClasses}>
      {children}
    </button>
  );
};
