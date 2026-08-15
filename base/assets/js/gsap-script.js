document.addEventListener("DOMContentLoaded", function () {
    gsap.registerPlugin(ScrollTrigger);

    cardBannerHomeAnimation();
    bannerHomeParallax();
    cardCompanyStatMiddle();
    cardServiceAnimation();
    aboutAnimation();
    chooseusImageFade();
    cardStackAnimation();
    contactCTAAnimation();
    bannerInnerParallax();
    serviceCTAParallax();
    contactCardAnimation();
});

function cardBannerHomeAnimation() {
    const card = document.querySelector(".card-banner-home");
    if (!card) return;

    // Guard di luar matchMedia agar tidak re-register saat refresh
    if (card.dataset.gsapParallax === "1") return;
    card.dataset.gsapParallax = "1";

    const mm = gsap.matchMedia();

    mm.add("(min-width: 768px)", () => {
        gsap.set(card, { x: 0 });

        gsap.to(card, {
            x: -70,
            ease: "none",
            scrollTrigger: {
                trigger: ".banner-home__layout",
                start: "top bottom",
                end: "bottom top",
                scrub: true,
                invalidateOnRefresh: true,
            }
        });

        return () => {
            gsap.set(card, { x: 0 });
        };
    });
}

function bannerHomeParallax() {
    const bg = document.querySelector(".banner-home-bg");

    if (!bg || bg.dataset.gsapParallax === "1") return;
    bg.dataset.gsapParallax = "1";

    gsap.fromTo(
        bg,
        { 
            scale: 1,
            y: 0
        },
        {
            scale: 1.5,
            y: -60,
            ease: "none",
            scrollTrigger: {
                trigger: ".banner-home-section",
                start: "top bottom",
                end: "bottom top",
                scrub: true,
                invalidateOnRefresh: true,
            }
        }
    );

    ScrollTrigger.refresh();
}

function cardCompanyStatMiddle() {
    const cardStat = document.querySelector(".card-company-stat.card-company-stat-middle");
    if (!cardStat || cardStat.dataset.gsapParallax === "1") return;
    cardStat.dataset.gsapParallax = "1";

    gsap.set(cardStat, { y: 55 });

    gsap.to(cardStat, {
        y: 0,
        ease: "none",
        scrollTrigger: {
            trigger: ".company-stat-section",
            start: "top bottom",
            end: "bottom top",
            scrub: true,
            invalidateOnRefresh: true,
        }
    });

    ScrollTrigger.refresh();
}

function cardServiceAnimation() {
    const cards = document.querySelectorAll(".card-service");

    if (!cards.length) return;

    cards.forEach((card, index) => {

        const bg = card.querySelector(".card-service--slide__bg");
        if (!bg) return;

        if (bg.dataset.gsapParallax === "1") return;
        bg.dataset.gsapParallax = "1";

        const isEven = index % 2 === 0;

        const fromY = isEven ? 70 : -70;
        const toY   = isEven ? -70 : 70;

        gsap.fromTo(
            bg,
            { y: fromY },
            {
                y: toY,
                ease: "none",
                scrollTrigger: {
                    trigger: card,
                    start: "top bottom",
                    end: "bottom top",
                    scrub: true,
                }
            }
        );
    });
}

function aboutAnimation() {
    const section = document.querySelector(".about__layout");
    if (!section) return;

    const imageLeft = section.querySelector(".image-left");
    const imageRight = section.querySelector(".image-right");
    const logo = section.querySelector(".circular-text");

    // prevent double init
    if (section.dataset.gsapInit === "1") return;
    section.dataset.gsapInit = "1";

    // =========================
    // IMAGE LEFT (turun)
    // =========================
    if (imageLeft) {
        gsap.fromTo(
            imageLeft,
            { y: 0 },
            {
                y: 55,
                ease: "none",
                scrollTrigger: {
                    trigger: section,
                    start: "top bottom",
                    end: "bottom top",
                    scrub: true,
                }
            }
        );
    }

    // =========================
    // IMAGE RIGHT (naik)
    // =========================
    if (imageRight) {
        gsap.fromTo(
            imageRight,
            { y: 0 },
            {
                y: -55,
                ease: "none",
                scrollTrigger: {
                    trigger: section,
                    start: "top bottom",
                    end: "bottom top",
                    scrub: true,
                }
            }
        );
    }

    // =========================
    // TEXT ROTATE (FIXED 🔥)
    // =========================
    if (logo) {
        gsap.fromTo(
            logo,
            { rotate: 0 },
            {
                rotate: 180, // bisa ubah ke 360 kalau mau full spin
                ease: "none",
                scrollTrigger: {
                    trigger: section,
                    start: "top bottom",
                    end: "bottom top",
                    scrub: true,
                }
            }
        );
    }

    ScrollTrigger.refresh();
}

function chooseusImageFade() {
    const image = document.querySelector(".why-choose-us__image-intro");

    if (!image) return;

    if (image.dataset.gsapInit === "1") return;
    image.dataset.gsapInit = "1";

    gsap.from(image, {
        opacity: 0,
        y: 50,
        duration: 1,
        ease: "power2.out",
        scrollTrigger: {
            trigger: image,
            start: "top 80%",
            toggleActions: "play none none reverse"
        }
    });
}

function cardStackAnimation() {
    const container = document.querySelector(".project__card-container");
    if (!container) return;

    const cards = container.querySelectorAll(".card-project");
    if (!cards.length) return;

    function init() {
        ScrollTrigger.getAll()
            .filter(st => st.vars?.id === "cardStack")
            .forEach(st => st.kill());

        gsap.set(cards, { clearProps: "all" });
        container.style.position = "";
        container.style.height = "";

        const cardHeight = cards[0].offsetHeight;
        if (!cardHeight) return;

        const gap = 20;
        const overlap = 0.8;

        container.style.position = "relative";
        container.style.height = cardHeight + "px";

        cards.forEach((card, i) => {
            gsap.set(card, {
                position: "absolute",
                top: i * (cardHeight + gap),
                left: 0,
                width: "100%",
                zIndex: i + 1,
                transformOrigin: "top center",
            });
        });

        const scrollSteps = cards.length - 1;
        const scrollPerStep = window.innerHeight * 0.5;

        const tl = gsap.timeline({
            scrollTrigger: {
                id: "cardStack",
                trigger: ".project__layout",
                start: "top top",
                end: `+=${scrollSteps * scrollPerStep}`,
                scrub: 1,
                pin: true,
                anticipatePin: 1,
                invalidateOnRefresh: true,
            }
        });

        cards.forEach((card, i) => {
            if (i === cards.length - 1) return;

            const nextCard = cards[i + 1];
            const nextNaturalTop = (i + 1) * (cardHeight + gap);

            // ✅ SEMUA card (kecuali last karena tidak masuk loop) tetap scale
            tl.to(card, {
                scale: 0.9,
                duration: 0.4,
                ease: "power2.inOut",
            });

            tl.fromTo(
                nextCard,
                { y: 0 },
                {
                    y: -nextNaturalTop * overlap,
                    duration: 0.6,
                    ease: "power2.inOut"
                },
                "<0.1"
            );
        });

        // ✅ Final stacking tetap smooth
        tl.to(cards, {
            y: (i) => -i * (cardHeight + gap),
            duration: 0.6,
            ease: "power2.inOut"
        });
    }

    init();

    let resizeTimer;
    window.addEventListener("resize", () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            init();
            ScrollTrigger.refresh();
        }, 250);
    });
}

function contactCTAAnimation() {
    const section = document.querySelector(".contact-cta__layout");
    const imageBg = document.querySelector(".contact-cta__image-bg");

    if (!section || !imageBg) return;

    // prevent double init
    if (section.dataset.gsapInit === "1") return;
    section.dataset.gsapInit = "1";

    gsap.fromTo(
        imageBg,
        {
            x: -70,
            scale: 1.1
        },
        {
            x: 0,
            scale: 1,
            ease: "none",
            scrollTrigger: {
                trigger: section,
                start: "top 80%",
                end: "bottom top",
                scrub: true,
            }
        }
    );
}

function bannerInnerParallax() {
    const section = document.querySelector(".banner-inner-section");
    const bg = document.querySelector(".banner-inner-bg");

    if (!section || !bg) return;

    if (bg.dataset.gsapInit === "1") return;
    bg.dataset.gsapInit = "1";

    gsap.fromTo(
        bg,
        { 
            y: -60,
            scale: 1.3
        },
        {
            y: 0,
            scale: 1,
            ease: "none",
            scrollTrigger: {
                trigger: section,
                start: "top bottom",
                end: "bottom top",
                scrub: true,
            }
        }
    );
}

function serviceCTAParallax() {
    const section = document.querySelector(".section-service-cta");
    const bg = document.querySelector(".service-cta-bg");

    if (!section || !bg) return;

    if (bg.dataset.gsapInit === "1") return;
    bg.dataset.gsapInit = "1";

    gsap.fromTo(
        bg,
        { 
            y: -60,
            scale: 1.5
        },
        {
            y: 0,
            scale: 1,
            ease: "none",
            scrollTrigger: {
                trigger: section,
                start: "top bottom",
                end: "bottom top",
                scrub: true,
            }
        }
    );
}

function contactCardAnimation() {
    const section = document.querySelector(".card-contact-page");
    const imageBg = document.querySelector(".contact-image-bg");

    if (!section || !imageBg) return;

    // prevent double init
    if (section.dataset.gsapInit === "1") return;
    section.dataset.gsapInit = "1";

    gsap.fromTo(
        imageBg,
        {
            x: -70,
            scale: 1.3
        },
        {
            x: 0,
            scale: 1,
            ease: "none",
            scrollTrigger: {
                trigger: section,
                start: "top 80%",
                end: "bottom top",
                scrub: true,
            }
        }
    );
}

window.addEventListener("load", () => {
    ScrollTrigger.refresh();
});