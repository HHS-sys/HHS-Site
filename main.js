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
    addStylesheet("/styles.css?v=20260818-5", "core-style-fallback");
  }

  addStylesheet("/mobile-fixes.css?v=20260818-5", "mobile-layout-fixes");
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
  link.addEventListener("click", () => {
    // Let Safari complete the link's default navigation before hiding its ancestor.
    window.setTimeout(() => setNavigation(false), 0);
  });
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
if ("IntersectionObserver" in window && revealElements.length) {
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
  document.documentElement.classList.add("reveal-ready");
} else {
  revealElements.forEach((element) => element.classList.add("is-visible"));
}

const mobileActions = document.querySelector(".mobile-actions");
const siteFooter = document.querySelector(".site-footer");
const quoteForm = document.querySelector("#quote-form");

if (mobileActions && "IntersectionObserver" in window) {
  const mobileActionsMedia = window.matchMedia("(max-width: 620px)");
  let footerIsNearViewport = false;
  let quoteFormIsVisible = false;

  const updateMobileActionsVisibility = () => {
    const shouldHide =
      mobileActionsMedia.matches && (footerIsNearViewport || quoteFormIsVisible);
    mobileActions.classList.toggle("is-context-hidden", shouldHide);
    mobileActions.toggleAttribute("inert", shouldHide);
    if (shouldHide) {
      mobileActions.setAttribute("aria-hidden", "true");
    } else {
      mobileActions.removeAttribute("aria-hidden");
    }
  };

  if (siteFooter) {
    const footerObserver = new IntersectionObserver(
      ([entry]) => {
        footerIsNearViewport = entry.isIntersecting;
        updateMobileActionsVisibility();
      },
      { rootMargin: "0px 0px 72px 0px", threshold: 0 },
    );
    footerObserver.observe(siteFooter);
  }

  if (quoteForm) {
    const quoteFormObserver = new IntersectionObserver(
      ([entry]) => {
        quoteFormIsVisible = entry.isIntersecting;
        updateMobileActionsVisibility();
      },
      { rootMargin: "0px 0px -12% 0px", threshold: 0 },
    );
    quoteFormObserver.observe(quoteForm);
  }
  if (typeof mobileActionsMedia.addEventListener === "function") {
    mobileActionsMedia.addEventListener("change", updateMobileActionsVisibility);
  } else if (typeof mobileActionsMedia.addListener === "function") {
    mobileActionsMedia.addListener(updateMobileActionsVisibility);
  }
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

const formError = quoteForm?.querySelector("[data-form-error]");
const quoteHandoff = quoteForm?.querySelector("[data-quote-handoff]");
const quoteSuccess = quoteForm?.querySelector("[data-quote-success]");
const quoteEmailLink = quoteForm?.querySelector("[data-quote-email]");
const quoteCopyButton = quoteForm?.querySelector("[data-copy-quote]");
const quoteCopyStatus = quoteForm?.querySelector("[data-copy-status]");
const quoteSubmitButton = quoteForm?.querySelector("[data-quote-submit]");
const quoteSubmitLabel = quoteForm?.querySelector("[data-submit-label]");
const quoteSubmissionId = quoteForm?.querySelector("[data-submission-id]");
let preparedQuoteText = "";
let quoteIsSubmitting = false;

function createSubmissionId() {
  if (typeof globalThis.crypto?.randomUUID === "function") {
    return globalThis.crypto.randomUUID();
  }

  const bytes = new Uint8Array(16);
  globalThis.crypto.getRandomValues(bytes);
  bytes[6] = (bytes[6] & 0x0f) | 0x40;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  const hex = [...bytes].map((byte) => byte.toString(16).padStart(2, "0"));
  return `${hex.slice(0, 4).join("")}-${hex.slice(4, 6).join("")}-${hex.slice(6, 8).join("")}-${hex.slice(8, 10).join("")}-${hex.slice(10).join("")}`;
}

function refreshSubmissionId() {
  if (quoteSubmissionId) quoteSubmissionId.value = createSubmissionId();
}

function setQuoteSubmitting(isSubmitting) {
  quoteIsSubmitting = isSubmitting;
  quoteForm?.toggleAttribute("aria-busy", isSubmitting);
  quoteForm
    ?.querySelectorAll("input, select, textarea")
    .forEach((control) => {
      control.disabled = isSubmitting;
    });
  if (quoteSubmitButton) quoteSubmitButton.disabled = isSubmitting;
  if (quoteSubmitLabel) {
    quoteSubmitLabel.textContent = isSubmitting ? "Sending…" : "Send enquiry";
  }
}

refreshSubmissionId();

function hideQuoteHandoff() {
  if (quoteHandoff) quoteHandoff.hidden = true;
  if (quoteSuccess) quoteSuccess.hidden = true;
  preparedQuoteText = "";
  if (quoteCopyStatus) quoteCopyStatus.textContent = "";
}

quoteForm?.addEventListener("input", () => {
  if (quoteIsSubmitting) return;
  hideQuoteHandoff();
  if (formError) formError.textContent = "";
  refreshSubmissionId();
});

quoteForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (quoteIsSubmitting) return;
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

  if (phone && phone.replace(/\D/g, "").length < 7) {
    if (formError) {
      formError.textContent = "Please enter a complete phone number, or leave it blank and use your email address.";
    }
    quoteForm.elements.phone.focus();
    return;
  }

  if (formError) formError.textContent = "";
  if (quoteHandoff) quoteHandoff.hidden = true;
  if (quoteSuccess) quoteSuccess.hidden = true;

  preparedQuoteText = `Name: ${data.get("name") || ""}
Phone: ${phone}
Email: ${email}
Project location: ${data.get("location") || ""}
Project type: ${data.get("service") || ""}
Preferred timing: ${data.get("timing") || ""}

Project details:
${data.get("message") || ""}`;

  const subject = encodeURIComponent(
    "Website quote request - Hekman Home Services",
  );
  const body = encodeURIComponent(preparedQuoteText);

  if (quoteEmailLink) {
    quoteEmailLink.href = `mailto:hekmanhomeservices@gmail.com?subject=${subject}&body=${body}`;
  }
  if (quoteCopyStatus) quoteCopyStatus.textContent = "";

  setQuoteSubmitting(true);

  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 12000);

  try {
    const response = await fetch(quoteForm.action, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(Object.fromEntries(data.entries())),
      credentials: "same-origin",
      signal: controller.signal,
    });

    let result = null;
    try {
      result = await response.json();
    } catch {
      // A non-JSON response is never accepted as a successful enquiry.
    }
    if (!response.ok || result?.ok !== true) {
      const error = new Error(
        result?.error || "We could not confirm that your enquiry was sent.",
      );
      error.status = response.status;
      throw error;
    }

    quoteForm.reset();
    refreshSubmissionId();
    preparedQuoteText = "";
    if (quoteSuccess) {
      quoteSuccess.hidden = false;
      quoteSuccess.focus({ preventScroll: true });
      quoteSuccess.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
    if (typeof window.va === "function") {
      window.va("event", { name: "Quote Enquiry Sent" });
    }
  } catch (error) {
    if (formError) {
      formError.textContent =
        error?.status >= 400 && error.status < 500
          ? error.message
          : "We could not send your enquiry online. Your details are still here—please try again or use a direct contact option below.";
    }
    if (quoteHandoff) {
      quoteHandoff.hidden = false;
      quoteHandoff.focus({ preventScroll: true });
      quoteHandoff.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  } finally {
    window.clearTimeout(timeout);
    setQuoteSubmitting(false);
  }
});

quoteCopyButton?.addEventListener("click", async () => {
  if (!preparedQuoteText) return;

  try {
    await navigator.clipboard.writeText(preparedQuoteText);
    if (quoteCopyStatus) {
      quoteCopyStatus.textContent =
        "Copied. Paste the details into any email, text or message.";
    }
  } catch {
    const copyArea = document.createElement("textarea");
    copyArea.value = preparedQuoteText;
    copyArea.setAttribute("readonly", "");
    copyArea.style.position = "fixed";
    copyArea.style.opacity = "0";
    document.body.appendChild(copyArea);
    copyArea.select();
    const copied = document.execCommand("copy");
    copyArea.remove();

    if (quoteCopyStatus) {
      quoteCopyStatus.textContent = copied
        ? "Copied. Paste the details into any email, text or message."
        : "Copy was unavailable. Please use the email, call or text options below.";
    }
  }
});
