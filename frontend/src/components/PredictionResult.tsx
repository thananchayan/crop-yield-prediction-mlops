import type { PredictionResponse } from "../types/prediction";

type PredictionResultProps = {
  result: PredictionResponse;
};

const formatPrediction = (value: number): string =>
  new Intl.NumberFormat("en", {
    maximumFractionDigits: 2,
  }).format(value);

export function PredictionResult({ result }: PredictionResultProps) {
  return (
    <section className="result-panel" aria-live="polite">
      <div>
        <span className="eyebrow">Predicted yield</span>
        <p className="prediction-value">
          {formatPrediction(result.prediction)}
          <span>{result.unit}</span>
        </p>
      </div>
      <dl className="result-meta">
        <div>
          <dt>Model</dt>
          <dd>{result.model_id}</dd>
        </div>
        <div>
          <dt>Version</dt>
          <dd>{result.model_version}</dd>
        </div>
        <div>
          <dt>Request</dt>
          <dd>{result.request_id}</dd>
        </div>
      </dl>
    </section>
  );
}
