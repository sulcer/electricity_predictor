'use client';
import React, {FC} from 'react';
import {useProduction} from "@/lib/hooks/prediction-service";
import {capitalizeFirstLetter, mapTableData} from "@/utils/utils";
import {DataTable} from "@/components/ui/data-table";

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
                {isLoading ? <p>Loading...</p> : <DataTable columns={columns} data={mapTableData(production)}/>}
            </div>
        </div>
    );
};

export default ProductionInfo;