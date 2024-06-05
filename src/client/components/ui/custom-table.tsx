import React, {FC} from 'react';
import {mapTableData} from "@/utils/utils";
import {DataTable} from "@/components/home/prediction-table";


interface CustomTableProps {
    columns: any[];
    data: any;
}


const CustomTable: FC<CustomTableProps> = ({ columns, data}) => {
    return (
        <>
            <DataTable columns={columns} data={mapTableData(data)} />
        </>
    );
};

export default CustomTable;