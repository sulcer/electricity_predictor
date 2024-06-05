'use client'
import React, {FC} from 'react';
import PriceInfo from "@/components/home/price-info";
import PredictionInfo from "@/components/home/prediction-info";
import Link from "next/link";
import {Home} from "lucide-react";
import ProductionInfo from "@/components/home/production-info";

interface DetailsProps {
    model_type: string;
}

const Details: FC<DetailsProps> = ({ model_type }) => {
    console.log(model_type)
    return (
        <div className={'mt-3 mx-10'}>
            <Link href={'/'}>
                <Home color="grey" size={20} />
            </Link>
            {model_type === 'price' ? <PriceInfo /> : <ProductionInfo production_type={model_type.split("_")[1]} />}
            <PredictionInfo modelType={model_type} number={24}/>
        </div>
    );
};

export default Details;