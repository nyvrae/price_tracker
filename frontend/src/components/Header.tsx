import Image from "next/image";
import { ShoppingCartOutlined, MenuOutlined } from '@ant-design/icons';

import Link from "next/link";

export default function Header() {
    return (
        <header className="flex items-center justify-center pt-6">
            <div className="flex items-center justify-evenly bg-white text-white w-[20svw] max-w-[500px] min-w-[300px] rounded-full px-4">
                <div className="flex-shrink-0">
                    <a href="/" aria-label="Go to homepage">
                        <Image
                            src="/logo2.png"
                            alt="Price Tracker Logo"
                            width={50}
                            height={50}
                        />
                    </a>
                </div>

                <div className="flex-1 text-center">
                    <Link
                        href={"/dashboard"}
                        className="relative font-bebas tracking-wider text-xl hover:text-accent transition-all duration-300 inline-block text-sub group"
                    >
                        Dashboard
                    </Link>
                </div>

                <div className="flex items-center gap-2">
                    <button aria-label="View shopping cart" className="rounded hover:bg-sub/10 p-1">
                        <ShoppingCartOutlined style={{ color: '#110b11', fontSize: '24px' }} />
                    </button>
                    <button aria-label="Open menu" className="rounded hover:bg-sub/10 p-1">
                        <MenuOutlined style={{ color: '#110b11', fontSize: '24px' }} />
                    </button>
                </div>
            </div>
        </header>
    );
}
