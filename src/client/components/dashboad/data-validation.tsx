import React from 'react';
import {transformLinkName} from "@/utils/utils";
import Link from "next/link";

const prediction_types = [
    'price',
    'production_cross',
    'production_fossil',
    'production_hydro',
    'production_nuclear',
]

const DataValidation = () => {
    return (
        <div className={' flex flex-col items-center mt-5'}>
            <h3 className={'text-xl font-bold my-3'}>Data Validation Reports</h3>
            <div className={'flex flex-row gap-x-5'}>
                {prediction_types.map((modelType) => {
                    return (
                        <div key={modelType}>
                            <Link
                                className={"font-bold hover:text-blue-600 hover:drop-shadow-2xl  transition duration-300"}
                                href={`https://electricy-predictor-reports.netlify.app/${modelType}_data_drift.html`}>{transformLinkName(modelType)} Data
                                Drift</Link>
                        </div>
                    );
                })}
            </div>
            <div className={'flex flex-row gap-x-5'}>
                {prediction_types.map((modelType) => {
                    return (

                        <div key={modelType}>
                            <Link
                                className={"font-bold hover:text-blue-600 hover:drop-shadow-2xl  transition duration-300"}
                                href={`https://electricy-predictor-reports.netlify.app/${modelType}_data_stability_tests.html`}>{transformLinkName(modelType)} Stability
                                Test</Link>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default DataValidation;