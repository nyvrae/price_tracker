import Image from "next/image";
import Link from "next/link";

type ItemLinkProps = {
    title: string;
    url: string;
    price: string | number | null | undefined;
    image_url?: string;
    date?: string;
};

export default function ItemLink({ title, url, price, image_url, date }: ItemLinkProps) {
    const displayPrice =
        price !== null && price !== undefined && String(price) !== "null" && String(price).trim() !== ""
            ? `$${price}`
            : "—";

    const displayTitle = title.length > 30 ? title.slice(0, 30) + "..." : title;

    return (
        <div className="block w-full max-w-4xl px-2">
            <div className="flex flex-wrap items-center gap-3 rounded-2xl bg-white text-black shadow-md hover:shadow-lg transition-shadow p-3">

                {image_url && (
                    <div className="relative flex-shrink-0 w-16 h-16 sm:w-20 sm:h-20 md:w-24 md:h-24 rounded-lg overflow-hidden border">
                        <Image
                            src={image_url}
                            alt={title}
                            fill
                            className="object-cover"
                        />
                    </div>
                )}

                <div className="flex flex-col flex-1 min-w-[100px] overflow-hidden">
                    {date && <p className="text-xs sm:text-sm text-gray-500 truncate">{date}</p>}
                    <p className="font-semibold text-sm sm:text-base md:text-lg truncate" title={title}>
                        {displayTitle}
                    </p>
                    <p className="text-sm sm:text-base font-medium mt-1">{displayPrice}</p>
                </div>

                <div className="flex flex-nowrap flex-shrink-0 mt-2 sm:mt-0 gap-2">
                    <Link href={url} className="px-3 py-1 text-sm sm:text-base bg-accent text-white rounded-lg hover:opacity-90">
                        Explore
                    </Link>
                    <button className="px-3 py-1 text-sm sm:text-base bg-accent text-white rounded-lg hover:opacity-90 cursor-pointer">
                        Add
                    </button>
                </div>
            </div>
        </div>
    );
}
