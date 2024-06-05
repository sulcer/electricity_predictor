import React from 'react';
import Details from "@/components/home/details";

interface PageProps {
    params: {
        model_type: string;
    }
}

const Page = ({ params }: PageProps) => {
    return (
        <div>
            <Details model_type={params.model_type} />
        </div>
    );
};

export default Page;