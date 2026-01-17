interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
}) => {
  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex justify-center items-center w-full h-full bg-black/50"
      onClick={onClose}
    >
      <div
        className="relative p-4 w-full max-w-xl max-h-full"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="relative bg-surface border border-border rounded-base shadow-sm p-4 md:p-6">
          <div className="flex items-center justify-between border-b border-border pb-4 md:pb-5">
            <h3 className="text-lg font-medium text-heading">{title}</h3>
            <button
              type="button"
              onClick={onClose}
              className="text-body bg-transparent hover:bg-neutral-tertiary hover:text-heading rounded-base text-sm w-9 h-9 ms-auto inline-flex justify-center items-center"
            >
              <svg
                className="w-5 h-5"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                fill="none"
                viewBox="0 0 24 24"
              >
                <path
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M6 18 17.94 6M18 18 6.06 6"
                />
              </svg>
              <span className="sr-only">Close modal</span>
            </button>
          </div>
          <div className="pt-4 md:pt-6">{children}</div>
        </div>
      </div>
    </div>
  );
};
