/**
 * Types for the NER Agent API
 * API: https://ner-backend-171009084156.europe-west1.run.app
 */

export type NERPredictRequest = {
  text: string;
};

export type NEREntity = {
  start: number;
  end: number;
  label: string;
  text: string;
};

export type NERRawPrediction = {
  token: string;
  label: string;
  score: number;
};

export type NERPredictResponse = {
  entities: NEREntity[];
  raw_predictions: NERRawPrediction[];
};
