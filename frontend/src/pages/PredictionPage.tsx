import { useState } from "react";

import { predictCropYield, PredictionApiError } from "../api/predictionApi";
import { ErrorMessage } from "../components/ErrorMessage";
import { PredictionForm } from "../components/PredictionForm";
import { PredictionResult } from "../components/PredictionResult";
import type { PredictionRequest, PredictionResponse } from "../types/prediction";

type PageError = {
  message: string;
  requestId?: string;
};

export function PredictionPage() {
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<PageError | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handlePrediction = async (payload: PredictionRequest) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await predictCropYield(payload);
      setResult(response);
    } catch (caughtError) {
      if (caughtError instanceof PredictionApiError) {
        setError({
          message: caughtError.message,
          requestId: caughtError.requestId,
        });
      } else {
        setError({ message: "Unexpected frontend error." });
      }
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="app-shell">
      <section className="workspace" aria-labelledby="page-title">
        <div className="page-header">
          <div>
            <span className="eyebrow">ML inference console</span>
            <h1 id="page-title">Crop Yield Prediction</h1>
          </div>
          <div className="status-pill">
            <span aria-hidden="true" />
            FastAPI connected
          </div>
        </div>

        <div className="content-grid">
          <section className="form-panel" aria-label="Prediction input form">
            <PredictionForm
              isSubmitting={isLoading}
              onSubmit={handlePrediction}
            />
          </section>

          <aside className="output-panel" aria-label="Prediction output">
            {error ? (
              <ErrorMessage message={error.message} requestId={error.requestId} />
            ) : null}

            {result ? (
              <PredictionResult result={result} />
            ) : (
              <div className="empty-state">
                <span className="empty-state-icon" aria-hidden="true">
                  %
                </span>
                <h2>Awaiting prediction</h2>
                <p>
                  Submit crop and climate inputs to receive a yield estimate
                  from the deployed model.
                </p>
              </div>
            )}
          </aside>
        </div>
      </section>
    </main>
  );
}
