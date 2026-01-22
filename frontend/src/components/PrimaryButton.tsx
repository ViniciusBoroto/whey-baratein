export const PrimaryButton = ({
  children,
  onClick,
  className = "",
  type = "button",
}: {
  children: React.ReactNode;
  onClick?: (e: React.MouseEvent) => void;
  className?: string;
  type?: "button" | "submit" | "reset";
}) => {
  const baseClasses =
    "bg-brand hover:bg-brand-hover text-white font-bold py-2 px-4 rounded-base transition duration-180 hover:scale-103 hover:shadow-lg hover:-translate-y-1 hover:shadow-border";
  const composedClasses = `${baseClasses} ${className || ""}`.trim();

  return (
    <button type={type} onClick={onClick} className={composedClasses}>
      {children}
    </button>
  );
};
