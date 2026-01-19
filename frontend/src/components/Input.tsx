interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  id: string;
  wrapperClassName?: string;
}

export const Input: React.FC<InputProps> = ({ label, id, wrapperClassName, ...props }) => {
  return (
    <div className={`mb-4 ${wrapperClassName || ''}`}>
      <label htmlFor={id} className="block mb-2.5 text-sm font-medium text-heading">
        {label}
      </label>
      <input
        id={id}
        className="bg-surface-strong border border-border-light text-heading text-sm rounded-base focus:ring-brand focus:border-brand block w-full px-3 py-2.5 shadow-xs placeholder:text-body"
        {...props}
      />
    </div>
  );
};
