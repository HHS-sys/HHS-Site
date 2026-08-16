document.querySelectorAll("[data-year]").forEach((element) => {
  element.textContent = new Date().getFullYear();
});

const navToggle = document.querySelector(".nav-toggle");
const primaryNav = document.querySelector(".primary-nav");

function setNavigation(open) {
  if (!navToggle || !primaryNav) return;
  navToggle.setAttribute("aria-expanded", String(open));
  primaryNav.classList.toggle("is-open", open);
  document.body.classList.toggle("nav-open", open);
}

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

window.matchMedia("(min-width: 861px)").addEventListener("change", (event) => {
  if (event.matches) setNavigation(false);
});

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

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const selected = button.dataset.filter;
    let visibleCount = 0;

    filterButtons.forEach((candidate) => {
      const active = candidate === button;
      candidate.classList.toggle("active", active);
      candidate.setAttribute("aria-pressed", String(active));
    });

    projectCards.forEach((card) => {
      const categories = (card.dataset.category || "").split(/\s+/);
      const visible =
        selected === "all" || categories.includes(selected);
      card.classList.toggle("is-hidden", !visible);
      if (visible) visibleCount += 1;
    });

    if (filterStatus) {
      filterStatus.textContent =
        selected === "all"
          ? `Showing all ${visibleCount} photographs.`
          : `Showing ${visibleCount} photographs in ${button.textContent.trim()}.`;
    }
  });
});

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
    lightbox.showModal();
  });
});

lightboxClose?.addEventListener("click", () => lightbox.close());
lightbox?.addEventListener("click", (event) => {
  if (event.target === lightbox) lightbox.close();
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
