document.documentElement.classList.add("js");

(function ensureSiteStyles() {
  const addStylesheet = (href, id) => {
    if (document.getElementById(id)) return;
    const link = document.createElement("link");
    link.id = id;
    link.rel = "stylesheet";
    link.href = href;
    document.head.appendChild(link);
  };

  const coreStylesLoaded = getComputedStyle(document.documentElement)
    .getPropertyValue("--deep")
    .trim();

  if (!coreStylesLoaded) {
    addStylesheet("/styles.css?v=20260816-1", "core-style-fallback");
  }

  addStylesheet("/mobile-fixes.css?v=20260816-1", "mobile-layout-fixes");
})();

document.querySelectorAll("[data-year]").forEach((element) => {
  element.textContent = new Date().getFullYear();
});

const navToggle = document.querySelector(".nav-toggle");
const primaryNav = document.querySelector(".primary-nav");
const mobileNavMedia = window.matchMedia("(max-width: 860px)");

function setNavigation(open) {
  if (!navToggle || !primaryNav) return;

  const nextOpen = Boolean(open && mobileNavMedia.matches);
  navToggle.setAttribute("aria-expanded", String(nextOpen));
  primaryNav.classList.toggle("is-open", nextOpen);
  primaryNav.hidden = mobileNavMedia.matches ? !nextOpen : false;
  document.body.classList.toggle("nav-open", nextOpen);
}

setNavigation(false);

navToggle?.addEventListener("click", () => {
  setNavigation(navToggle.getAttribute("aria-expanded") !== "true");
});

primaryNav?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => setNavigation(false));
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") setNavigation(false);
});

document.addEventListener("click", (event) => {
  if (
    navToggle?.getAttribute("aria-expanded") === "true" &&
    !primaryNav?.contains(event.target) &&
    !navToggle.contains(event.target)
  ) {
    setNavigation(false);
  }
});

const handleNavigationBreakpoint = () => setNavigation(false);
if (typeof mobileNavMedia.addEventListener === "function") {
  mobileNavMedia.addEventListener("change", handleNavigationBreakpoint);
} else if (typeof mobileNavMedia.addListener === "function") {
  mobileNavMedia.addListener(handleNavigationBreakpoint);
}

window.addEventListener("orientationchange", () => setNavigation(false));

const revealElements = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries, currentObserver) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          currentObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.08 },
  );
  revealElements.forEach((element) => observer.observe(element));
} else {
  revealElements.forEach((element) => element.classList.add("is-visible"));
}

const filterButtons = document.querySelectorAll("[data-filter]");
const projectCards = document.querySelectorAll("[data-category]");
const filterStatus = document.querySelector("[data-filter-status]");
const loadMoreButton = document.querySelector("[data-load-more]");
const galleryPageSize = 18;
const moreCategories = new Set(["flooring", "drywall", "insulation", "structural"]);
let selectedProjectFilter = "all";
let galleryVisibleLimit = galleryPageSize;

function matchesProjectFilter(card, selected) {
  const categories = (card.dataset.category || "").split(/\s+/);
  if (selected === "all") return true;
  if (selected === "more") {
    return categories.some((category) => moreCategories.has(category));
  }
  return categories.includes(selected);
}

function updateProjectGallery() {
  const matchingCards = Array.from(projectCards).filter((card) =>
    matchesProjectFilter(card, selectedProjectFilter),
  );
  const visibleCount = Math.min(galleryVisibleLimit, matchingCards.length);
  const activeButton = Array.from(filterButtons).find(
    (button) => button.dataset.filter === selectedProjectFilter,
  );

  projectCards.forEach((card) => {
    const matches = matchesProjectFilter(card, selectedProjectFilter);
    const matchIndex = matchingCards.indexOf(card);
    card.classList.toggle("is-hidden", !matches);
    card.classList.toggle(
      "is-collapsed",
      matches && matchIndex >= galleryVisibleLimit,
    );
  });

  if (filterStatus) {
    const categoryName = activeButton?.textContent.trim();
    filterStatus.textContent =
      selectedProjectFilter === "all"
        ? `Showing ${visibleCount} of ${matchingCards.length} photographs.`
        : `Showing ${visibleCount} of ${matchingCards.length} photographs in ${categoryName}.`;
  }

  if (loadMoreButton) {
    loadMoreButton.hidden = visibleCount >= matchingCards.length;
  }
}

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    selectedProjectFilter = button.dataset.filter || "all";
    galleryVisibleLimit = galleryPageSize;

    filterButtons.forEach((candidate) => {
      const active = candidate === button;
      candidate.classList.toggle("active", active);
      candidate.setAttribute("aria-pressed", String(active));
    });

    updateProjectGallery();
  });
});

loadMoreButton?.addEventListener("click", () => {
  galleryVisibleLimit += galleryPageSize;
  updateProjectGallery();
});

updateProjectGallery();

const lightbox = document.querySelector("[data-lightbox-dialog]");
const lightboxImage = lightbox?.querySelector("img");
const lightboxCaption = lightbox?.querySelector("p");
const lightboxClose = lightbox?.querySelector("[data-lightbox-close]");

document.querySelectorAll("[data-lightbox]").forEach((button) => {
  button.addEventListener("click", () => {
    const sourceImage = button.querySelector("img");
    const caption = button.closest("figure")?.querySelector("figcaption span");
    if (!lightbox || !lightboxImage || !sourceImage) return;

    lightboxImage.src = sourceImage.currentSrc || sourceImage.src;
    lightboxImage.alt = sourceImage.alt;
    if (lightboxCaption) lightboxCaption.textContent = caption?.textContent || "";

    if (typeof lightbox.showModal === "function") {
      lightbox.showModal();
    } else {
      lightbox.setAttribute("open", "");
    }
  });
});

function closeLightbox() {
  if (!lightbox) return;
  if (typeof lightbox.close === "function") {
    lightbox.close();
  } else {
    lightbox.removeAttribute("open");
  }
}

lightboxClose?.addEventListener("click", closeLightbox);
lightbox?.addEventListener("click", (event) => {
  if (event.target === lightbox) closeLightbox();
});

const quoteForm = document.querySelector("#quote-form");
const formError = quoteForm?.querySelector("[data-form-error]");

quoteForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!quoteForm.checkValidity()) {
    quoteForm.reportValidity();
    return;
  }

  const data = new FormData(quoteForm);
  const phone = String(data.get("phone") || "").trim();
  const email = String(data.get("email") || "").trim();

  if (!phone && !email) {
    if (formError) {
      formError.textContent =
        "Please enter a phone number, an email address, or both.";
    }
    quoteForm.elements.phone.focus();
    return;
  }

  if (formError) formError.textContent = "";

  const subject = encodeURIComponent(
    "Website quote request - Hekman Home Services",
  );
  const body = encodeURIComponent(
    `Name: ${data.get("name") || ""}
Phone: ${phone}
Email: ${email}
Project location: ${data.get("location") || ""}
Project type: ${data.get("service") || ""}
Preferred timing: ${data.get("timing") || ""}

Project details:
${data.get("message") || ""}`,
  );

  window.location.href = `mailto:hekmanhomeservices@gmail.com?subject=${subject}&body=${body}`;
});
