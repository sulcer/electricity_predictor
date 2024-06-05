'use client';
import React from 'react';
import {usePrice} from "@/lib/hooks/prediction-service";

const Info = () => {
    const { data: price } = usePrice();

    return (
        <div>
            Infos about prediction service
        </div>
    );
};

export default Info;