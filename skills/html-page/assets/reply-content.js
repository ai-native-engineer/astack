(() => {
	let restoring = false;
	let savedForms = [];
	let lastState = "";
	let scheduled = false;
	let headings = [];
	let outlineState = "";
	let activeHeading = -1;
	let positionScheduled = false;
	let bottomSpace = 0;
	let questionState = "";
	const spacers = new Map();
	const sourceStyle = document.createElement("style");
	sourceStyle.textContent =
		".html-reply-end-space{display:block!important;flex:none!important;grid-column:1/-1!important;width:1px!important;min-width:0!important;pointer-events:none!important;visibility:hidden!important;margin:0!important;padding:0!important;border:0!important}";
	document.head.append(sourceStyle);
	function isVisible(node) {
		return (
			node.getClientRects().length &&
			getComputedStyle(node).visibility !== "hidden"
		);
	}
	function scrollParent(node) {
		for (
			let current = node.parentElement;
			current && current !== document.body;
			current = current.parentElement
		) {
			if (/(auto|scroll)/.test(getComputedStyle(current).overflowY))
				return current;
		}
		return document.scrollingElement;
	}
	function updateSpace() {
		const roots = new Set();
		for (const node of [...headings, ...sections()]) {
			const root = scrollParent(node);
			if (root)
				roots.add(root === document.scrollingElement ? document.body : root);
		}
		if (!roots.size) roots.add(document.body);
		for (const [root, spacer] of spacers) {
			if (!roots.has(root)) {
				spacer.remove();
				spacers.delete(root);
			}
		}
		for (const root of roots) {
			let spacer = spacers.get(root);
			if (!spacer) {
				spacer = document.createElement("div");
				spacer.className = "html-reply-end-space";
				spacer.setAttribute("aria-hidden", "true");
				spacers.set(root, spacer);
			}
			if (root.lastElementChild !== spacer) root.append(spacer);
			spacer.style.height = `${bottomSpace}px`;
			spacer.style.minHeight = `${bottomSpace}px`;
		}
	}
	function updatePosition() {
		positionScheduled = false;
		const visible = headings
			.map((heading, key) => ({ heading, key }))
			.filter(({ heading }) => isVisible(heading));
		let active = visible[0]?.key ?? -1;
		for (const { heading, key } of visible) {
			const root = scrollParent(heading);
			const top =
				root === document.scrollingElement
					? 0
					: root.getBoundingClientRect().top;
			const atEnd =
				root.scrollHeight > root.clientHeight + 2 &&
				root.scrollTop + root.clientHeight >= root.scrollHeight - 2;
			if (heading.getBoundingClientRect().top <= top + 100 || atEnd)
				active = key;
		}
		if (active !== activeHeading) {
			activeHeading = active;
			parent.postMessage({ type: "html-reply-position", active }, "*");
		}
	}
	function schedulePosition() {
		if (positionScheduled) return;
		positionScheduled = true;
		requestAnimationFrame(updatePosition);
	}
	function updateOutline() {
		headings = [...document.querySelectorAll("h1,h2,h3")]
			.filter((heading) => isVisible(heading) && heading.textContent.trim())
			.slice(0, 200);
		const entries = headings.map((heading, key) => ({
			key,
			level: Number(heading.tagName[1]),
			text: heading.textContent.trim().replace(/\s+/g, " ").slice(0, 160),
			questionIds: sections()
				.filter((section) => {
					const anchor = section.querySelector("h1,h2,h3,legend") || section;
					const next = headings
						.slice(key + 1)
						.find(
							(node) => Number(node.tagName[1]) <= Number(heading.tagName[1]),
						);
					return (
						(anchor === heading ||
							!!(
								heading.compareDocumentPosition(anchor) &
								Node.DOCUMENT_POSITION_FOLLOWING
							)) &&
						(!next ||
							!!(
								anchor.compareDocumentPosition(next) &
								Node.DOCUMENT_POSITION_FOLLOWING
							))
					);
				})
				.map((section) => section.getAttribute("data-item")),
		}));
		const encoded = JSON.stringify(entries);
		if (encoded !== outlineState) {
			outlineState = encoded;
			parent.postMessage(
				{
					type: "html-reply-outline",
					headings: entries,
					active: activeHeading,
				},
				"*",
			);
		}
		updateSpace();
		schedulePosition();
	}
	function available(section) {
		for (
			let node = section;
			node && node !== document.body;
			node = node.parentElement
		) {
			if (
				node.hidden ||
				node.getAttribute("aria-hidden") === "true" ||
				getComputedStyle(node).display === "none" ||
				getComputedStyle(node).visibility === "hidden"
			)
				return false;
		}
		return true;
	}
	const allSections = () =>
		[...document.querySelectorAll("[data-item]")].filter(
			(section) => ownedFields(section).length,
		);
	const sections = () =>
		allSections().filter(
			(section) => available(section) && fields(section).length,
		);
	const ownedFields = (section) =>
		[
			...section.querySelectorAll(
				'input[type="radio"],input[type="checkbox"],input[type="text"],input[type="number"],textarea,select',
			),
		].filter(
			(field) =>
				field.closest("[data-item]") === section &&
				!field.matches(
					"textarea[data-reply-output],textarea#out[readonly],textarea#reply-text[readonly]",
				),
		);
	const fields = (section) =>
		ownedFields(section).filter(
			(field) =>
				!field.matches(":disabled") && !field.readOnly && available(field),
		);
	const fieldKey = (field, index) =>
		field.id ||
		(["radio", "checkbox"].includes(field.type)
			? `${field.name}:${field.value}`
			: field.name || String(index));

	function collect() {
		const items = sections().map((section) => {
			const id = section.getAttribute("data-item");
			const label =
				section.querySelector("h2,h3,h4,legend,label")?.textContent?.trim() ||
				id;
			const ownFields = fields(section);
			const values = ownFields
				.filter(
					(field) =>
						["radio", "checkbox"].includes(field.type) && field.checked,
				)
				.map((input) => input.value);
			for (const select of ownFields.filter(
				(field) => field.tagName === "SELECT",
			)) {
				for (const option of select.selectedOptions)
					if (option.value) values.push(option.value);
			}
			for (const input of ownFields.filter(
				(field) =>
					["text", "number"].includes(field.type) ||
					field.matches("textarea[data-reply-answer]"),
			)) {
				if (input.value.trim()) values.push(input.value.trim());
			}
			const memo = ownFields
				.filter((field) => field.matches("textarea:not([data-reply-answer])"))
				.map((input) => input.value.trim())
				.filter(Boolean)
				.join("\n");
			return { id, label, values, memo };
		});
		const forms = allSections().map((section) => ({
			id: section.getAttribute("data-item"),
			fields: ownedFields(section).map((field, index) => ({
				key: fieldKey(field, index),
				value: field.value,
				checked: field.checked,
				...(field.tagName === "SELECT" && field.multiple
					? {
							selected: [...field.selectedOptions].map(
								(option) => option.value,
							),
						}
					: {}),
			})),
		}));
		const sheet = items.length
			? ""
			: document.querySelector(
					"textarea[data-reply-output],textarea#out[readonly],textarea#reply-text[readonly]",
				)?.value || "";
		for (const saved of savedForms) {
			const current = forms.find((form) => form.id === saved.id);
			if (!current) forms.push(saved);
			else
				for (const field of saved.fields) {
					const index = current.fields.findIndex(
						(candidate) => candidate.key === field.key,
					);
					if (index < 0) current.fields.push(field);
					else current.fields[index] = field;
				}
		}
		return { items, forms, sheet, location: window.location.hash };
	}
	function reviewQuestions(items) {
		const questions = items.map((item) => ({
			id: item.id,
			label: item.label,
			state: item.values.length
				? "answered"
				: item.memo
					? "note"
					: "unanswered",
		}));
		const encoded = JSON.stringify(questions);
		if (encoded !== questionState) {
			questionState = encoded;
			parent.postMessage({ type: "html-reply-questions", questions }, "*");
		}
	}
	function navigate(target, focusAnswer = false) {
		if (!target) return;
		for (let node = target; node; node = node.parentElement) {
			if (node.tagName === "DETAILS") node.open = true;
		}
		target.scrollIntoView({
			block: "start",
			behavior: matchMedia("(prefers-reduced-motion: reduce)").matches
				? "instant"
				: "smooth",
		});
		const focus = focusAnswer ? fields(target)[0] || target : target;
		const hadTabindex = focus.hasAttribute("tabindex");
		if (!hadTabindex && !focus.matches("input,textarea,select,button")) {
			focus.tabIndex = -1;
			focus.addEventListener("blur", () => focus.removeAttribute("tabindex"), {
				once: true,
			});
		}
		focus.focus({ preventScroll: true });
		schedulePosition();
	}

	function context(quote) {
		if (restoring) return;
		const state = collect();
		reviewQuestions(state.items);
		const encoded = JSON.stringify(state);
		if (!quote && encoded === lastState) return;
		lastState = encoded;
		parent.postMessage(
			{ type: "html-reply-context", ...state, ...(quote ? { quote } : {}) },
			"*",
		);
	}

	function restore() {
		restoring = true;
		const waiting = [];
		for (const saved of savedForms) {
			const section = allSections().find(
				(item) => item.getAttribute("data-item") === saved.id,
			);
			if (!section || !Array.isArray(saved.fields)) {
				waiting.push(saved);
				continue;
			}
			const matched = new Set();
			ownedFields(section).forEach((field, index) => {
				const value =
					saved.fields.find(
						(candidate) => candidate.key === fieldKey(field, index),
					) || (!saved.fields[index]?.key ? saved.fields[index] : null);
				if (!value) return;
				if (field.tagName === "SELECT") {
					const desired =
						field.multiple && Array.isArray(value.selected)
							? value.selected
							: value.value
								? [value.value]
								: [];
					if (
						desired.some(
							(option) =>
								![...field.options].some(
									(candidate) => candidate.value === option,
								),
						)
					)
						return;
				}
				matched.add(value);
				if (["radio", "checkbox"].includes(field.type))
					field.checked = !!value.checked;
				else if (
					field.tagName === "SELECT" &&
					field.multiple &&
					Array.isArray(value.selected)
				) {
					for (const option of field.options)
						option.selected = value.selected.includes(option.value);
				} else if (typeof value.value === "string") field.value = value.value;
				field.dispatchEvent(new Event("input", { bubbles: true }));
				field.dispatchEvent(new Event("change", { bubbles: true }));
			});
			const missing = saved.fields.filter((field) => !matched.has(field));
			if (missing.length) waiting.push({ ...saved, fields: missing });
		}
		savedForms = waiting;
		restoring = false;
		context();
	}

	document.addEventListener("mouseup", () =>
		context(window.getSelection()?.toString()),
	);
	function discardPendingField(field) {
		const section = field.closest("[data-item]");
		if (!section) return;
		const key = fieldKey(field, ownedFields(section).indexOf(field));
		for (const saved of savedForms) {
			if (saved.id === section.getAttribute("data-item"))
				saved.fields = saved.fields.filter(
					(candidate) => candidate.key !== key,
				);
		}
		savedForms = savedForms.filter((saved) => saved.fields.length);
	}
	document.addEventListener("input", (event) => {
		if (!restoring) discardPendingField(event.target);
		context();
	});
	document.addEventListener("focusin", (event) => {
		const section = event.target.closest("[data-item]");
		if (section && available(section))
			parent.postMessage(
				{
					type: "html-reply-question-focus",
					id: section.getAttribute("data-item"),
				},
				"*",
			);
	});
	document.addEventListener("change", (event) => {
		const input = event.target;
		if (!restoring) discardPendingField(input);
		if (input.matches('input[type="checkbox"]') && input.checked) {
			const section = input.closest("[data-item]");
			if (section) {
				for (const peer of fields(section)) {
					if (
						peer !== input &&
						peer.type === "checkbox" &&
						(input.hasAttribute("data-reply-exclusive") ||
							peer.hasAttribute("data-reply-exclusive"))
					)
						peer.checked = false;
				}
			}
		}
		context();
	});
	window.addEventListener("hashchange", () => context());
	window.addEventListener("message", (event) => {
		if (event.source !== parent) return;
		if (event.data?.type === "html-reply-layout") {
			if (Number.isFinite(event.data.bottom)) {
				bottomSpace = Math.max(0, Math.min(2000, event.data.bottom));
				updateSpace();
			}
			return;
		}
		if (event.data?.type === "html-reply-navigate") {
			const heading = Number.isInteger(event.data.key)
				? headings[event.data.key]
				: null;
			if (heading && isVisible(heading)) navigate(heading);
			return;
		}
		if (event.data?.type === "html-reply-question") {
			const section = sections().find(
				(item) => item.getAttribute("data-item") === event.data.id,
			);
			if (section) navigate(section, true);
			return;
		}
		if (event.data?.type !== "html-reply-restore") return;
		savedForms = Array.isArray(event.data.forms) ? event.data.forms : [];
		restore();
		updateOutline();
	});
	// React/Babel artifacts can mount their controls after the bridge loads.
	new MutationObserver((records) => {
		if (
			records.every(
				(record) =>
					record.target.classList?.contains("html-reply-end-space") ||
					(record.type === "childList" &&
						[...record.addedNodes, ...record.removedNodes].every(
							(node) =>
								node.nodeType === 1 &&
								node.classList.contains("html-reply-end-space"),
						)),
			)
		)
			return;
		if (scheduled || restoring) return;
		scheduled = true;
		requestAnimationFrame(() => {
			scheduled = false;
			if (savedForms.length) restore();
			else context();
			updateOutline();
		});
	}).observe(document.body, {
		childList: true,
		subtree: true,
		characterData: true,
		attributes: true,
		attributeFilter: [
			"hidden",
			"class",
			"aria-hidden",
			"open",
			"style",
			"disabled",
			"readonly",
		],
	});
	document.addEventListener("scroll", schedulePosition, {
		capture: true,
		passive: true,
	});
	document.documentElement.addEventListener("pointerenter", () =>
		parent.postMessage({ type: "html-reply-source-pointer" }, "*"),
	);
	window.addEventListener("resize", updateOutline);
	document.addEventListener("change", updateOutline);
	parent.postMessage({ type: "html-reply-ready" }, "*");
	updateOutline();
})();
