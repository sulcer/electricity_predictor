'use client';
import React from 'react';
import {usePrice} from "@/lib/hooks/prediction-service";
import CustomTable from "@/components/ui/custom-table";

const columns = [
  {
    accessorKey: 'date',
    header: 'Date',
  },
  {
    accessorKey: 'value',
    header: 'Price',
  },
];

const PriceInfo = () => {
    const { data: price, isLoading, isError } = usePrice();

    return (
        <div className={'w-1/3 mt-5'}>
            <div>
                {isLoading ? <p>Loading...</p> : <CustomTable columns={columns} data={price} />}
            </div>
        </div>
    );
};

export default PriceInfo;