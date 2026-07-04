import axios from "axios";

import { httpClient } from "./httpClient";
import type {
  ApiErrorResponse,
  PredictionRequest,
  PredictionResponse,
} from "../types/prediction";

export class PredictionApiError extends Error {
  status?: number;
  code?: string;
  requestId?: string;

  constructor(message: string, options?: { status?: number; code?: string; requestId?: string }) {
    super(message);
    this.name = "PredictionApiError";
    this.status = options?.status;
    this.code = options?.code;
    this.requestId = options?.requestId;
  }
}

export const predictCropYield = async (
  payload: PredictionRequest,
): Promise<PredictionResponse> => {
  try {
    const response = await httpClient.post<PredictionResponse>("/predict", payload);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError<ApiErrorResponse>(error)) {
      const responseData = error.response?.data;
      throw new PredictionApiError(
        responseData?.error?.message ??
          "Prediction request failed. Check the backend service.",
        {
          status: error.response?.status,
          code: responseData?.error?.code,
          requestId: responseData?.request_id,
        },
      );
    }

    throw new PredictionApiError("Unexpected prediction error.");
  }
};
