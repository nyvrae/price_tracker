import Image from "next/image";
import { ShoppingCartOutlined, MenuOutlined } from '@ant-design/icons';

import Link from "next/link";

export default function Header() {
    return (
        <header className="flex items-center justify-evenly px-32 py-8 bg-back text-text">
            <div className="flex-shrink-0">
                <a href="/" aria-label="Go to homepage">
                    <Image
                        src="/logo_cutted.png"
                        alt="Price Tracker Logo"
                        width={50}
                        height={50}
                    />
                </a>
            </div>

            <div className="flex-1 text-center">
                <Link
                    href={"/dashboard"}
                    className="relative font-bebas tracking-widest text-2xl hover:tracking-wider transition-all duration-300 inline-block text-text group"
                >
                    Dashboard
                    <span className="absolute left-0 -bottom-[2px] h-[2px] w-0 bg-text transition-all duration-300 group-hover:w-full"></span>
                </Link>
            </div>

            <div className="flex items-center gap-4">
                <button aria-label="View shopping cart" className="p-2 rounded hover:bg-white/10 transition-colors hover:cursor-pointer">
                    <ShoppingCartOutlined className="text-3xl" />
                </button>
                <button aria-label="Open menu" className="p-2 rounded hover:bg-white/10 transition-colors hover:cursor-pointer">
                    <MenuOutlined className="text-3xl" />
                </button>
            </div>
        </header>
    );
}
