import { useState } from "react";

import { Button } from "./Button";
import { TextInput } from "./TextInput";
import type {
  FieldErrors,
  PredictionFormValues,
  PredictionRequest,
} from "../types/prediction";
import {
  hasValidationErrors,
  toPredictionRequest,
  validatePredictionForm,
} from "../utils/validators";

const initialValues: PredictionFormValues = {
  area: "Albania",
  item: "Maize",
  year: "1990",
  averageRainFallMmPerYear: "1485",
  pesticidesTonnes: "121",
  avgTemp: "16.37",
};

type PredictionFormProps = {
  isSubmitting: boolean;
  onSubmit: (payload: PredictionRequest) => Promise<void>;
};

export function PredictionForm({ isSubmitting, onSubmit }: PredictionFormProps) {
  const [values, setValues] = useState<PredictionFormValues>(initialValues);
  const [errors, setErrors] = useState<FieldErrors>({});

  const updateField =
    (field: keyof PredictionFormValues) =>
    (event: React.ChangeEvent<HTMLInputElement>) => {
      setValues((current) => ({ ...current, [field]: event.target.value }));
      setErrors((current) => ({ ...current, [field]: undefined }));
    };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const validationErrors = validatePredictionForm(values);
    setErrors(validationErrors);

    if (hasValidationErrors(validationErrors)) {
      return;
    }

    await onSubmit(toPredictionRequest(values));
  };

  return (
    <form className="prediction-form" onSubmit={handleSubmit} noValidate>
      <div className="form-grid">
        <TextInput
          id="area"
          label="Area"
          value={values.area}
          error={errors.area}
          onChange={updateField("area")}
          autoComplete="country-name"
        />
        <TextInput
          id="item"
          label="Crop"
          value={values.item}
          error={errors.item}
          onChange={updateField("item")}
          autoComplete="off"
        />
        <TextInput
          id="year"
          label="Year"
          type="number"
          value={values.year}
          error={errors.year}
          onChange={updateField("year")}
          min={1900}
          max={2100}
        />
        <TextInput
          id="rainfall"
          label="Average rainfall (mm/year)"
          type="number"
          value={values.averageRainFallMmPerYear}
          error={errors.averageRainFallMmPerYear}
          onChange={updateField("averageRainFallMmPerYear")}
          min={0}
          step="0.01"
        />
        <TextInput
          id="pesticides"
          label="Pesticides (tonnes)"
          type="number"
          value={values.pesticidesTonnes}
          error={errors.pesticidesTonnes}
          onChange={updateField("pesticidesTonnes")}
          min={0}
          step="0.01"
        />
        <TextInput
          id="temperature"
          label="Average temperature (C)"
          type="number"
          value={values.avgTemp}
          error={errors.avgTemp}
          onChange={updateField("avgTemp")}
          min={-50}
          max={60}
          step="0.01"
        />
      </div>

      <div className="form-actions">
        <Button type="submit" isLoading={isSubmitting}>
          {isSubmitting ? "Predicting" : "Predict yield"}
        </Button>
      </div>
    </form>
  );
}
