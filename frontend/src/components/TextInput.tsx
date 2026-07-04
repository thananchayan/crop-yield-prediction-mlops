import type { InputHTMLAttributes } from "react";

type TextInputProps = InputHTMLAttributes<HTMLInputElement> & {
  label: string;
  error?: string;
};

export function TextInput({ id, label, error, ...props }: TextInputProps) {
  const errorId = error && id ? `${id}-error` : undefined;

  return (
    <label className="field" htmlFor={id}>
      <span className="field-label">{label}</span>
      <input
        id={id}
        className={error ? "input input-error" : "input"}
        aria-invalid={Boolean(error)}
        aria-describedby={errorId}
        {...props}
      />
      {error ? (
        <span className="field-error" id={errorId}>
          {error}
        </span>
      ) : null}
    </label>
  );
}
