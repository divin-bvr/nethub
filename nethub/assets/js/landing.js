(() => {
	const dialog = document.querySelector('#login-dialog');
	const form = document.querySelector('#login-form');
	const errorMessage = document.querySelector('#login-error');
	const memberResources = document.querySelector('#member-resources');
	const hero = document.querySelector('.hero');
	const heroPhoto = document.querySelector('.hero-photo');
	const year = document.querySelector('#copyright-year');
	let scrollFrame = 0;

	if (year) year.textContent = new Date().getFullYear();

	if ('IntersectionObserver' in window) {
		document.documentElement.classList.add('motion-ready');
		const revealObserver = new IntersectionObserver((entries, observer) => {
			entries.forEach(entry => {
				if (!entry.isIntersecting) return;
				entry.target.classList.add('is-visible');
				observer.unobserve(entry.target);
			});
		}, { threshold: 0.12 });
		document.querySelectorAll('[data-reveal]').forEach(element => revealObserver.observe(element));
	}

	function updateHeroFade() {
		scrollFrame = 0;
		if (!hero || !heroPhoto) return;
		const fadeDistance = Math.max(hero.offsetHeight * 0.9, 1);
		const progress = Math.min(Math.max(window.scrollY / fadeDistance, 0), 1);
		heroPhoto.style.setProperty('--hero-photo-opacity', String(1 - progress * 0.72));
	}

	window.addEventListener('scroll', () => {
		if (!scrollFrame) scrollFrame = window.requestAnimationFrame(updateHeroFade);
	}, { passive: true });
	updateHeroFade();

	document.querySelectorAll('[data-open-login]').forEach(button => {
		button.addEventListener('click', () => {
			errorMessage.textContent = '';
			dialog.showModal();
			dialog.querySelector('#login-username').focus();
		});
	});

	document.querySelector('[data-close-login]').addEventListener('click', () => dialog.close());
	dialog.addEventListener('click', event => {
		if (event.target === dialog) dialog.close();
	});

	form.addEventListener('submit', event => {
		event.preventDefault();
		const values = new FormData(form);
		const username = String(values.get('username') || '').trim();
		const password = String(values.get('password') || '');

		if (username !== 'admin' || password !== '1234') {
			errorMessage.textContent = 'Those login details were not recognized.';
			form.elements.password.value = '';
			form.elements.password.focus();
			return;
		}

		sessionStorage.setItem('nethub-demo-authorized', 'true');
		memberResources.hidden = false;
		errorMessage.textContent = '';
		form.reset();
		dialog.close();
		memberResources.scrollIntoView({ behavior: 'smooth', block: 'center' });
	});

	if (sessionStorage.getItem('nethub-demo-authorized') === 'true') {
		memberResources.hidden = false;
	}

	document.querySelector('[data-logout]').addEventListener('click', () => {
		sessionStorage.removeItem('nethub-demo-authorized');
		memberResources.hidden = true;
		document.querySelector('#member-access').scrollIntoView({ behavior: 'smooth', block: 'center' });
	});
})();
