import './globals.css';
import StoreProvider from './StoreProvider';

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
        <StoreProvider>
            <html lang="en">
                <body>
                    <main>
                        {children}
                    </main>
                </body>
            </html>
        </StoreProvider>
    );
}