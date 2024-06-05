'use client';
import React, {FC} from 'react';
import {useProduction} from "@/lib/hooks/prediction-service";
import CustomTable from "@/components/ui/custom-table";
import {capitalizeFirstLetter} from "@/utils/utils";

const columns = [
    {
        accessorKey: 'date',
        header: 'Date',
    },
    {
        accessorKey: 'value',
        header: 'Production',
    },
];

interface ProductionInfoProps {
    production_type: string
}

const ProductionInfo: FC<ProductionInfoProps> = ({ production_type }) => {
    const {data: production, isLoading, isError} = useProduction(production_type);

    console.log(production);

    return (
        <div className={'w-1/3 mt-5'}>
            <h1 className={'text-xl font-bold'}>{capitalizeFirstLetter(production_type)} Production</h1>
            <div>
                {isLoading ? <p>Loading...</p> : <CustomTable columns={columns} data={production}/>}
            </div>
        </div>
    );
};

export default ProductionInfo;