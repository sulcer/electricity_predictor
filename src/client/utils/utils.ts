export const unixToLocalDatetime = (unixTime: number) => {
    const date = new Date(unixTime * 1000);
    return date.toLocaleString();
}

export const mapTableData = (data: any) => {
    const mappedData: any = [];
    data.map((d: any) => {
        mappedData.push({
            date: unixToLocalDatetime(d[0]),
            value: d[1]
        });
    });

    return mappedData;
}

export const capitalizeFirstLetter = (word: string) => {
    return word.charAt(0).toUpperCase() + word.slice(1);
}