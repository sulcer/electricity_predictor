'use client';
import React, {FC} from 'react';
import {useProduction} from "@/lib/hooks/prediction-service";
import {mapTableData, prepareDataAndLabelsForChart, transformLinkName} from "@/utils/utils";
import {DataTable} from "@/components/ui/data-table";
import LineChart from "@/components/ui/line-chart";
import LoadingSpinner from "@/components/ui/loading-spinner";

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

const ProductionInfo: FC<ProductionInfoProps> = ({production_type}) => {
    const {data: production, isLoading, isError} = useProduction(production_type);

    return (
        <div className={' w-full'}>
            {isLoading ? <LoadingSpinner/> : <><h3 className={'text-xl font-bold mt-10'}>Data
                for {transformLinkName(production_type)} Production</h3>
                <div className="flex justify-center items-center gap-20">
                    <div className="flex-1">
                        <DataTable columns={columns} data={mapTableData(production)}/>
                    </div>
                    <div className="flex-1">
                        <LineChart chart_data={prepareDataAndLabelsForChart(production)} label={'Actual values'}/>
                    </div>
                </div>
            </>}
        </div>
    );
};

export default ProductionInfo;