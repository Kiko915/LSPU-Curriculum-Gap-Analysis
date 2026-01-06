export function Footer() {
    return (
        <footer className="border-t border-border/40 py-8 md:py-0 md:px-8 bg-background/50">
            <div className="container flex flex-col items-center justify-between gap-2 md:h-24 md:flex-row md:gap-4">
                <p className="text-balance text-center text-sm font-medium leading-loose text-muted-foreground md:text-center">
                    Built by{" "}
                    <a
                        href="#"
                        target="_blank"
                        rel="noreferrer"
                        className="font-medium underline underline-offset-4"
                    >
                        DheKode
                    </a>
                    . Powered by A.S.P.I.R.E.
                </p>
                <p className="text-balance text-center text-sm leading-loose text-muted-foreground md:text-right">
                    &copy; {new Date().getFullYear()} All rights reserved.
                </p>
            </div>
        </footer>
    )
}
