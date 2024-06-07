'use client';
import TrainExperiments from "@/components/dashboad/train-experiments";
import ValidateExperiments from "@/components/dashboad/validate-experiments";
import DataValidation from "@/components/dashboad/data-validation";
import Link from "next/link";
import {Home} from "lucide-react";
import React from "react";

const Page = () => {
    return (
        <>
            <div className={'mt-3 flex items-center justify-between'}>
                <Link href={'/'}>
                    <Home color="grey" size={20} className={'mx-5'}/>
                </Link>
                <h1 className={'text-3xl font-bold text-center flex-1'}>Electricity Predictor Dashboard</h1>
            </div>
            <DataValidation/>
            <TrainExperiments/>
            <ValidateExperiments/>
        </>
    );
};

export default Page;