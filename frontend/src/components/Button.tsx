import type { ButtonHTMLAttributes, ReactNode } from "react";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  isLoading?: boolean;
};

export function Button({
  children,
  className = "",
  disabled,
  isLoading = false,
  ...props
}: ButtonProps) {
  return (
    <button
      className={`button ${className}`.trim()}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? <span className="spinner" aria-hidden="true" /> : null}
      <span>{children}</span>
    </button>
  );
}
