import React from 'react';
import Link from "next/link";

const Navbar = () => {
    return (
        <div className={'flex flex-1 justify-between m-5'}>
            <div>
                <h1 className={'text-2xl font-bold'}>Energy Production</h1>
            </div>
            <div>
                <h3 className={'text-lg font-semibold'}><Link href={'/dashboard'}>Dashboard</Link></h3>
            </div>
        </div>
    );
};

export default Navbar;