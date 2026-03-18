/**
 * Content Loader - Charge le contenu dynamique depuis l'API
 * Utilisé sur toutes les pages du site pour afficher le contenu géré via le CMS
 */

// Déterminer l'URL de l'API automatiquement
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5000/api'
    : 'https://bains-opera.onrender.com/api';

// Cache pour éviter de recharger les données à chaque fois
let settingsCache = null;
let carouselCache = null;

/**
 * Charge et applique les paramètres du site
 */
async function loadSiteSettings() {
    if (settingsCache) {
        applySiteSettings(settingsCache);
        return;
    }

    try {
        const response = await fetch(`${API_URL}/cms/settings`);
        const settings = await response.json();
        settingsCache = settings;
        applySiteSettings(settings);
    } catch (error) {
        console.error('Erreur lors du chargement des paramètres:', error);
    }
}

/**
 * Applique les paramètres du site aux éléments de la page
 */
function applySiteSettings(settings) {
    // Mise à jour des horaires dans la section info-bar
    const hoursElement = document.querySelector('.info-bar .info-item:nth-child(2) p');
    if (hoursElement && settings.hours_mercredi) {
        hoursElement.innerHTML = `
            Mercredi : ${settings.hours_mercredi || 'Fermé'}<br>
            Jeudi : ${settings.hours_jeudi || 'Fermé'}<br>
            Samedi : ${settings.hours_samedi || 'Fermé'}<br>
            Vendredi : ${settings.hours_vendredi || 'Fermé'}<br>
            Fermé Dimanche - Mardi
        `;
    }

    // Mise à jour de l'adresse
    const addressElement = document.querySelector('.info-bar .info-item:nth-child(1) p');
    if (addressElement && settings.address) {
        addressElement.innerHTML = settings.address.replace(',', '<br>');
    }

    // Mise à jour du contact
    const contactElement = document.querySelector('.info-bar .info-item:nth-child(3) p');
    if (contactElement && settings.email) {
        contactElement.innerHTML = `Réservation par mail<br>${settings.email}`;
    }

    // Mise à jour du footer
    const footerAbout = document.querySelector('footer .footer-section:first-child p');
    if (footerAbout && settings.footer_about) {
        footerAbout.textContent = settings.footer_about;
    }

    const footerContact = document.querySelector('footer .footer-section:last-child');
    if (footerContact && settings.address && settings.email) {
        const addressP = footerContact.querySelector('p:first-of-type');
        const emailP = footerContact.querySelector('p:last-of-type');
        if (addressP) addressP.innerHTML = settings.address.replace(',', '<br>');
        if (emailP) emailP.textContent = settings.email;
    }
}

/**
 * Charge et affiche les images du carousel
 */
async function loadCarousel() {
    if (carouselCache) {
        applyCarousel(carouselCache);
        return;
    }

    try {
        const response = await fetch(`${API_URL}/cms/carousel`);
        const images = await response.json();
        carouselCache = images;
        applyCarousel(images);
    } catch (error) {
        console.error('Erreur lors du chargement du carousel:', error);
    }
}

/**
 * Applique les images du carousel à la page
 */
function applyCarousel(images) {
    const carouselContainer = document.querySelector('.carousel-container');
    if (!carouselContainer || images.length === 0) return;

    // Effacer le contenu existant
    carouselContainer.innerHTML = '';

    // Créer les slides
    images.forEach((img, index) => {
        const slide = document.createElement('div');
        slide.className = `carousel-slide ${index === 0 ? 'active' : ''}`;
        slide.style.backgroundImage = `url('${img.image_url}')`;

        slide.innerHTML = `
            <div class="hero-content">
                <h1>${img.title}</h1>
                <p>${img.subtitle}</p>
                ${img.button_text ? `<a href="${img.button_link || '#'}" class="btn">${img.button_text}</a>` : ''}
            </div>
        `;

        carouselContainer.appendChild(slide);
    });

    // Ajouter les boutons de navigation
    const prevBtn = document.createElement('button');
    prevBtn.className = 'carousel-btn prev';
    prevBtn.innerHTML = '‹';
    prevBtn.onclick = () => changeSlide(-1);

    const nextBtn = document.createElement('button');
    nextBtn.className = 'carousel-btn next';
    nextBtn.innerHTML = '›';
    nextBtn.onclick = () => changeSlide(1);

    carouselContainer.appendChild(prevBtn);
    carouselContainer.appendChild(nextBtn);

    // Ajouter les indicateurs
    const indicators = document.createElement('div');
    indicators.className = 'carousel-indicators';

    images.forEach((_, index) => {
        const indicator = document.createElement('button');
        indicator.className = `indicator ${index === 0 ? 'active' : ''}`;
        indicator.onclick = () => goToSlide(index);
        indicators.appendChild(indicator);
    });

    carouselContainer.appendChild(indicators);

    // Réinitialiser le carousel
    initCarouselFunctionality();
}

/**
 * Initialise la fonctionnalité du carousel (autoplay, swipe, etc.)
 */
function initCarouselFunctionality() {
    let currentSlide = 0;
    const slides = document.querySelectorAll('.carousel-slide');
    const indicators = document.querySelectorAll('.indicator');
    let autoplayInterval;

    window.showSlide = function(index) {
        slides.forEach(slide => slide.classList.remove('active'));
        indicators.forEach(indicator => indicator.classList.remove('active'));

        if (index >= slides.length) {
            currentSlide = 0;
        } else if (index < 0) {
            currentSlide = slides.length - 1;
        } else {
            currentSlide = index;
        }

        slides[currentSlide].classList.add('active');
        indicators[currentSlide].classList.add('active');
    };

    window.changeSlide = function(direction) {
        showSlide(currentSlide + direction);
        resetAutoplay();
    };

    window.goToSlide = function(index) {
        showSlide(index);
        resetAutoplay();
    };

    function autoplay() {
        autoplayInterval = setInterval(() => {
            changeSlide(1);
        }, 5000);
    }

    function resetAutoplay() {
        clearInterval(autoplayInterval);
        autoplay();
    }

    // Démarrer l'autoplay
    autoplay();

    // Pause sur hover
    const carouselContainer = document.querySelector('.carousel-container');
    if (carouselContainer) {
        carouselContainer.addEventListener('mouseenter', () => {
            clearInterval(autoplayInterval);
        });

        carouselContainer.addEventListener('mouseleave', () => {
            autoplay();
        });

        // Support tactile pour mobile
        let touchStartX = 0;
        let touchEndX = 0;

        carouselContainer.addEventListener('touchstart', e => {
            touchStartX = e.changedTouches[0].screenX;
        });

        carouselContainer.addEventListener('touchend', e => {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        });

        function handleSwipe() {
            if (touchEndX < touchStartX - 50) {
                changeSlide(1);
            }
            if (touchEndX > touchStartX + 50) {
                changeSlide(-1);
            }
        }
    }
}

/**
 * Charge et affiche les offres spéciales
 */
async function loadSpecialOffers() {
    try {
        const response = await fetch(`${API_URL}/cms/offers`);
        const offers = await response.json();

        if (offers.length > 0) {
            displaySpecialOffers(offers);
        }
    } catch (error) {
        console.error('Erreur lors du chargement des offres:', error);
    }
}

/**
 * Affiche les offres spéciales sur la page
 */
function displaySpecialOffers(offers) {
    // Chercher une section dédiée ou créer une nouvelle section
    const ctaSection = document.querySelector('.cta-section');
    if (!ctaSection) return;

    // Créer une section pour les offres spéciales
    const offersSection = document.createElement('section');
    offersSection.className = 'special-offers-section';
    offersSection.style.cssText = 'background: #f8f9fa; padding: 3rem 2rem;';

    offersSection.innerHTML = `
        <div class="container">
            <h2 style="text-align: center; color: #D4915E; margin-bottom: 2rem;">Offres du Mois</h2>
            <div class="row g-4">
                ${offers.map(offer => `
                    <div class="col-12 col-md-6 col-lg-4">
                        <div class="card h-100" style="border: 2px solid #D4915E; border-radius: 8px;">
                            <div class="card-body">
                                <h5 class="card-title" style="color: #2C2C2C;">${offer.title}</h5>
                                <p class="card-text">${offer.description}</p>
                                ${offer.price ? `
                                    <div class="price" style="font-size: 1.5rem; font-weight: bold; color: #D4915E;">
                                        ${offer.price} €
                                        ${offer.old_price ? `<span style="text-decoration: line-through; font-size: 1rem; color: #6c757d; margin-left: 0.5rem;">${offer.old_price} €</span>` : ''}
                                    </div>
                                ` : ''}
                                ${offer.valid_until ? `
                                    <small class="text-muted">Valable jusqu'au ${new Date(offer.valid_until).toLocaleDateString('fr-FR')}</small>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;

    // Insérer avant la section CTA
    ctaSection.parentNode.insertBefore(offersSection, ctaSection);
}

/**
 * Initialise le chargement du contenu au chargement de la page
 */
document.addEventListener('DOMContentLoaded', () => {
    loadSiteSettings();

    // Charger le carousel uniquement sur la page d'accueil
    if (document.querySelector('.carousel-container')) {
        loadCarousel();
    }

    // Charger les offres spéciales sur la page d'accueil
    if (window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/')) {
        loadSpecialOffers();
    }
});
