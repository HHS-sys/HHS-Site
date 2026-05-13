
document.querySelector('form')?.addEventListener('submit', e => {
  e.preventDefault();
  const d = new FormData(e.target);
  const subject = encodeURIComponent('Website quote request - Hekman Home Services');
  const body = encodeURIComponent(
    `Name: ${d.get('name') || ''}\nContact: ${d.get('contact') || ''}\nService: ${d.get('service') || ''}\n\nProject Details:\n${d.get('message') || ''}`
  );
  window.location.href = `mailto:hekmanhomeservices@gmail.com?subject=${subject}&body=${body}`;
});
