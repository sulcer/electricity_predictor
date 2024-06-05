import { api } from '@/lib/axios';
import { AxiosResponse } from 'axios';
import {Prediction, Price, Production} from "@/lib/models";

export const getPrice = async () => {
    const res = (await api.get('/price')) as AxiosResponse<Price[]>;
    return res.data;
}

export const getProduction = async (production_type: string) => {
    const res = (await api.get(`/production/${production_type}`)) as AxiosResponse<Production[]>;
    return res.data;
}

export const getPredictions = async (model_type: string, numberOfPredictions: number) => {
    const res = (await api.get(`/predict/${model_type}/${numberOfPredictions}`)) as AxiosResponse<Prediction[]>;
    return res.data;
}