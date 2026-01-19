import React from "react";

type SquaredButtonProps = {
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
};

export const SquaredButton: React.FC<SquaredButtonProps> = ({
  children,
  onClick,
  className,
}) => {
  // Define your default/existent class names
  const baseClasses = `flex items-center text-body bg-neutral-primary-soft shadow-xs
  hover:bg-surface-alt hover:text-heading
  focus:ring-1 focus:ring-border-light focus:shadow-lg
  font-medium leading-5 rounded-xl text-full  p-2.5`;

  // Combine the base classes with the prop, ensuring a space is present
  const combinedClasses = `${baseClasses} ${className || ""}`.trim();

  return (
    <button onClick={onClick} className={combinedClasses}>
      {children}{" "}
    </button>
  );
};
