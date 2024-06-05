export const unixToLocalDatetime = (unixTime: number): string => {
    const date = new Date(unixTime * 1000);
    return date.toLocaleString();
}

export const mapTableData = (data: Array<Array<number>>) => {
    const mappedData: any = [];
    data.map((d: any) => {
        mappedData.push({
            date: unixToLocalDatetime(d[0]),
            value: d[1]
        });
    });

    return mappedData;
}

export const capitalizeFirstLetter = (word: string): string => {
    return word.charAt(0).toUpperCase() + word.slice(1);
}

export const prepareDataAndLabelsForChart = (data: Array<Array<number>> | any): [number[], string[]] => {
    const chartData: any = [];
    const tableData: any = [];

    data.map((d: any) => {
        chartData.push(d[1]);
        tableData.push(unixToLocalDatetime(d[0]).substring(11, 17));
    });

    return [chartData, tableData];
}
