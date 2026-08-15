document.addEventListener("DOMContentLoaded", function(){
    initNavLink();
    initAnimationScroll();
    initNavbarPopup();
    initCounter();
    initBannerIntro();
    initBannerPricingCta();
});

function initNavLink() {
    const currentUrl = window.location.href;

    document.querySelectorAll(".navbar-nav .nav-link").forEach(link => {
        if (link.href === currentUrl) {
            link.classList.add("active");
        }
    });

    document.querySelectorAll(".navbar-nav .dropdown-menu .dropdown-item").forEach(item => {
        if (item.href === currentUrl) {
            item.classList.add("active");

            const dropdown = item.closest(".dropdown");
            if (dropdown) {
                const toggle = dropdown.querySelector(".nav-link.dropdown-toggle");
                if (toggle) toggle.classList.add("active");
            }
        }
    });
}

function initAnimationScroll() {
    const elements = document.querySelectorAll('[data-animation]');
    const persistentAnimations = new Set([
        'fade-in','fade-left','fade-right','fade-up','fade-down'
    ]);

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;

            const el = entry.target;
            const animation = el.dataset.animation;
            const styles = getComputedStyle(el);

            const duration = el.dataset.duration || styles.getPropertyValue('--anim-duration').trim() || '1s';
            const delay = el.dataset.delay || styles.getPropertyValue('--anim-delay').trim() || '0s';

            el.style.animationName = animation;
            el.style.animationDuration = duration;
            el.style.animationDelay = delay;

            if (persistentAnimations.has(animation)) {
                el.style.animationFillMode = 'forwards';
                el.addEventListener('animationend', () => {
                    el.style.opacity = '1';

                    if (el.classList.contains('card-banner-home')) {
                        el.style.removeProperty('transform');
                        if (typeof window.cardBannerHomeAnimation === 'function') {
                            requestAnimationFrame(() => window.cardBannerHomeAnimation());
                        }
                    } else {
                        el.style.transform = 'none';
                    }
                }, { once: true });
            }

            el.style.animationPlayState = 'running';
            el.classList.add('animated');

            observer.unobserve(el);
        });
    }, { threshold: 0.1 });

    elements.forEach(el => {
        el.style.animationPlayState = 'paused';
        el.style.opacity = '0';
        observer.observe(el);
    });
}

function initNavbarPopup() {
    const btn = document.querySelector('.nav-btn');
    const popup = document.getElementById('navbarPopup');
    const dropdowns = document.querySelectorAll('.has-dropdown');

    // Toggle popup
    btn.addEventListener('click', function (e) {
        e.stopPropagation();
        popup.classList.toggle('active');
        btn.classList.toggle('active');

        // Icon switch for nav-btn when popup is active
        const icon = btn.querySelector('i');
        if (btn.classList.contains('active')) {
            if (icon) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-xmark', 'fa-solid');
            }
        } else {
            if (icon) {
                icon.classList.remove('fa-xmark');
                icon.classList.add('fa-bars');
            }
        }
    });

    // Dropdown toggle
    dropdowns.forEach(item => {
        const link = item.querySelector('a');

        link.addEventListener('click', function (e) {
            e.preventDefault();
            item.classList.toggle('active');
        });
    });

    // Close when click outside
    document.addEventListener('click', function (e) {
        if (!popup.contains(e.target) && !btn.contains(e.target)) {
            popup.classList.remove('active');
            btn.classList.remove('active');

            // Reset icon to fa-bars
            const icon = btn.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-xmark');
                icon.classList.add('fa-bars');
            }
        }
    });

    // Close when click link (optional)
    const links = popup.querySelectorAll('a:not(.has-dropdown > a)');
    links.forEach(link => {
        link.addEventListener('click', () => {
            popup.classList.remove('active');
            btn.classList.remove('active');

            // Reset icon to fa-bars
            const icon = btn.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-xmark');
                icon.classList.add('fa-bars');
            }
        });
    });
}

function initCounter() {
    const counters = document.querySelectorAll('.counter');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;

                const targetCount = parseFloat(el.dataset.count) || 0;
                const suffix = el.dataset.countSuffix || '';

                let currentCount = 0;

                const duration = 2000;
                const frameRate = 16;
                const totalFrames = duration / frameRate;
                const increment = targetCount / totalFrames;

                const counter = setInterval(() => {
                    currentCount += increment;

                    if (currentCount >= targetCount) {
                        currentCount = targetCount;
                        clearInterval(counter);
                    }

                    // Determine whether decimal values are needed
                    let displayValue;
                    if (targetCount % 1 !== 0) {
                        // If the target is a decimal → show 1 decimal place
                        displayValue = currentCount.toFixed(1);
                    } else {
                        displayValue = Math.floor(currentCount);
                    }

                    el.textContent = displayValue + suffix;
                }, frameRate);

                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    counters.forEach(counter => {
        observer.observe(counter);
    });
}

// Load YouTube API once
(function loadYouTubeAPI() {
    if (!window.YT) { // check if YT API already loaded
        const tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        const firstScriptTag = document.querySelector('script');
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }
})();

window.onYouTubeIframeAPIReadyQueue = [];

window.onYouTubeIframeAPIReady = function () {
    window.onYouTubeIframeAPIReadyQueue.forEach(cb => cb());
};

function initBannerIntro() {
    let player;

    window.onYouTubeIframeAPIReadyQueue.push(() => {
        player = new YT.Player('video-intro-background', {
            videoId: 'L9IaFr04LL0',
            playerVars: {
                autoplay: 1,
                controls: 0,
                mute: 1,
                loop: 1,
                playlist: 'L9IaFr04LL0',
                showinfo: 0,
                rel: 0,
                enablejsapi: 1,
                disablekb: 1,
                modestbranding: 1,
                iv_load_policy: 3,
                origin: window.location.origin
            },
            events: {
                onReady: onPlayerReady,
                onStateChange: onPlayerStateChange
            }
        });
    });

    function onPlayerReady(event) {
        event.target.playVideo();
        setYoutubeSize();
        window.addEventListener('resize', setYoutubeSize);
    }

    function onPlayerStateChange(event) {
        if (event.data === YT.PlayerState.ENDED) {
            player.playVideo();
        }
    }

    function setYoutubeSize() {
        const container = document.querySelector('.video-intro__content');
        if (!container) return;

        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;
        const aspectRatio = 16 / 9;

        let newWidth, newHeight;

        if (containerWidth / containerHeight > aspectRatio) {
            newWidth = containerWidth;
            newHeight = containerWidth / aspectRatio;
        } else {
            newWidth = containerHeight * aspectRatio;
            newHeight = containerHeight;
        }

        if (player && typeof player.getIframe === 'function') {
            const iframe = player.getIframe();
            iframe.width = newWidth;
            iframe.height = newHeight;
        }
    }
}

function initBannerPricingCta() {
    let player;

    window.onYouTubeIframeAPIReadyQueue.push(() => {
        player = new YT.Player('pricing-cta-bg', {
            videoId: 'L9IaFr04LL0',
            playerVars: {
                autoplay: 1,
                controls: 0,
                mute: 1,
                loop: 1,
                playlist: 'L9IaFr04LL0',
                showinfo: 0,
                rel: 0,
                enablejsapi: 1,
                disablekb: 1,
                modestbranding: 1,
                iv_load_policy: 3,
                origin: window.location.origin
            },
            events: {
                onReady: onPlayerReady,
                onStateChange: onPlayerStateChange
            }
        });
    });

    function onPlayerReady(event) {
        event.target.playVideo();
        setYoutubeSize();
        window.addEventListener('resize', setYoutubeSize);
    }

    function onPlayerStateChange(event) {
        if (event.data === YT.PlayerState.ENDED) {
            player.playVideo();
        }
    }

    function setYoutubeSize() {
        const container = document.querySelector('.pricing-cta__container');
        if (!container) return;

        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;
        const aspectRatio = 16 / 9;

        let newWidth, newHeight;

        if (containerWidth / containerHeight > aspectRatio) {
            newWidth = containerWidth;
            newHeight = containerWidth / aspectRatio;
        } else {
            newWidth = containerHeight * aspectRatio;
            newHeight = containerHeight;
        }

        if (player && typeof player.getIframe === 'function') {
            const iframe = player.getIframe();
            iframe.width = newWidth;
            iframe.height = newHeight;
        }
    }
}