from __future__ import annotations

def contact_page(*, SERVICES, SERVICE_DISPLAY_ORDER, hero, PHONE_LINK, PHONE_DISPLAY, EMAIL, section_heading, page) -> str:
    options = "".join(
        f'<option value="{SERVICES[slug]["name"]}">{SERVICES[slug]["name"]}</option>'
        for slug in SERVICE_DISPLAY_ORDER
    )
    body = f"""
    {hero("project-129.jpg", "Completed kitchen renovation", "Contact Hekman Home Services", "Tell us what you want to change.", "A short description, the project location and a few photos are enough to begin the conversation.", small=True, position="50% 58%")}
    <main id="main">
      <section class="section section-paper" id="quote"><div class="wrap contact-layout"><div class="contact-intro reveal"><p class="eyebrow">Request a quote</p><h2>Start with what you know.</h2><p>You do not need every finish or measurement decided. Tell us what is not working, what you would like the space to become and where the property is located.</p><div class="contact-direct"><h3>Prefer direct contact?</h3><a href="tel:{PHONE_LINK}"><small>Call or text</small><strong>{PHONE_DISPLAY}</strong></a><a href="mailto:{EMAIL}"><small>Email</small><strong>{EMAIL}</strong></a><div><small>Service area</small><strong>London &amp; nearby communities</strong></div></div></div>
      <form class="quote-form reveal" id="quote-form" novalidate><div class="form-heading"><span>Project enquiry</span><small>Fields marked * are required</small></div><div class="form-grid"><label>Name *<input name="name" autocomplete="name" required></label><label>Project location *<input name="location" autocomplete="address-level2" placeholder="London, Byron, St. Thomas…" required></label></div><fieldset><legend>How should we reach you? *</legend><p id="contact-help">Enter a phone number, an email address, or both.</p><div class="form-grid"><label>Phone<input name="phone" type="tel" autocomplete="tel"></label><label>Email<input name="email" type="email" autocomplete="email"></label></div></fieldset><div class="form-grid"><label>Project type<select name="service"><option value="">Choose one</option>{options}<option value="Multiple services / other">Multiple services / other</option></select></label><label>Preferred timing<input name="timing" placeholder="Flexible, this fall, as soon as possible…"></label></div><label>Project details *<textarea name="message" placeholder="What would you like repaired, renovated or changed?" required></textarea></label><p class="form-error" data-form-error role="alert"></p><button class="button button-dark" type="submit">Prepare Quote Email <span aria-hidden="true">↗</span></button><p class="form-note">This opens your email app with the details filled in so you can review and send them directly. You can attach project photos before sending.</p></form></div></section>
      <section class="section section-charcoal"><div class="wrap">{section_heading("What happens next", "A useful first conversation starts with context.", "Sharing a few details helps us understand the likely scope before arranging the next step.")}<ol class="process-grid compact-process"><li class="reveal"><h3>Describe the project</h3><p>Include the location, room and result you have in mind.</p></li><li class="reveal"><h3>Add photos</h3><p>Attach wide views and closer images of the affected areas.</p></li><li class="reveal"><h3>Connect</h3><p>We review the information and discuss the appropriate next step.</p></li></ol></div></section>
    </main>"""
    return page("Contact Hekman Home Services | Request a Quote", "Contact Hekman Home Services Inc. for renovation and repair projects in London, Ontario. Call 519-808-3312 or prepare a quote request by email.", "/contact/", "project-129.jpg", "contact", body, "contact-page")
def not_found_page(*, page) -> str:
    body = f"""
    <main id="main" class="not-found">
      <img src="/project-132.jpg" alt="" aria-hidden="true">
      <div class="not-found-shade"></div>
      <div class="not-found-content"><p class="eyebrow">404 · Page not found</p><h1>This page needs a little repair.</h1><p>The address may have changed, but the rest of the site is ready to explore.</p><div class="button-row"><a class="button button-primary" href="/">Return Home</a><a class="button button-ghost" href="/services/">Explore Services</a></div></div>
    </main>"""
    return page("Page Not Found | Hekman Home Services", "The requested page could not be found.", "/404.html", "project-132.jpg", "", body, "error-page", indexable=False)
def redirect_stub(destination: str, title: str, *, BASE_URL) -> str:
    canonical = f"{BASE_URL}{destination}"
    return f"""<!doctype html>
    <html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><meta name="robots" content="noindex"><link rel="canonical" href="{canonical}"><meta http-equiv="refresh" content="0; url={destination}"></head><body><p>This page has moved to <a href="{destination}">{destination}</a>.</p></body></html>"""

