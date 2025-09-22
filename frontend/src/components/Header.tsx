import Image from "next/image";
import { ShoppingCartOutlined, UserOutlined } from '@ant-design/icons';

import Link from "next/link";

export default function Header() {
    return (
        <header className="flex items-center justify-center pt-3 md:pt-6">
            <div className="flex items-center justify-evenly bg-accent text-white w-[20svw] max-w-[500px] min-w-[260px] rounded-full px-2 md:px-4">
                <div className="flex-shrink-0">
                    <a href="/" aria-label="Go to homepage">
                        <Image
                            src="/logo_cutted.png"
                            alt="Price Tracker Logo"
                            width={48}
                            height={48}
                        />
                    </a>
                </div>

                <div className="flex-1 text-center">
                    <Link
                        href={"/dashboard"}
                        className="relative font-bebas tracking-wider text-xl hover:text-sub transition-all duration-300 inline-block text-white group"
                    >
                        Dashboard
                    </Link>
                </div>

                <div className="flex items-center gap-1 md:gap-2">
                    <button aria-label="View shopping cart" className="rounded hover:bg-sub/25 hover:cursor-pointer p-1">
                        <ShoppingCartOutlined style={{ color: '#fff', fontSize: '24px' }} />
                    </button>
                    <button aria-label="Open menu" className="rounded hover:bg-sub/25 hover:cursor-pointer p-1">
                        <UserOutlined style={{ color: '#fff', fontSize: '24px' }} />
                    </button>
                </div>
            </div>
        </header>
    );
}
