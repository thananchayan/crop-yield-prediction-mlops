type ErrorMessageProps = {
  message: string;
  requestId?: string;
};

export function ErrorMessage({ message, requestId }: ErrorMessageProps) {
  return (
    <div className="alert alert-error" role="alert">
      <strong>Prediction failed</strong>
      <span>{message}</span>
      {requestId ? <small>Request ID: {requestId}</small> : null}
    </div>
  );
}
