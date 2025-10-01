import Header from "@/components/Header";
import Main from "@/components/Main";
import Footer from "@/components/Footer";

export default function Dashboard() {
    return (
        <section className="relative h-screen flex flex-col gap-15 md:gap-30">
            <Header />
            <Footer />
        </section>
    );
}
