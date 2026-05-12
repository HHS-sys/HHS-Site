
document.querySelectorAll('.filters button').forEach(btn=>btn.addEventListener('click',()=>{
 document.querySelectorAll('.filters button').forEach(b=>b.classList.remove('active'));btn.classList.add('active');
 const f=btn.dataset.filter;document.querySelectorAll('.tile').forEach(t=>t.style.display=(f==='all'||t.dataset.category===f)?'':'none');
}));
document.querySelector('form')?.addEventListener('submit',e=>{
 e.preventDefault();const d=new FormData(e.target);
 const subject=encodeURIComponent('Website quote request - Hekman Home Services');
 const body=encodeURIComponent(`Name: ${d.get('name')||''}\nContact: ${d.get('contact')||''}\nService: ${d.get('service')||''}\n\nProject Details:\n${d.get('message')||''}`);
 location.href=`mailto:hekmanhomeservices@gmail.com?subject=${subject}&body=${body}`;
});
