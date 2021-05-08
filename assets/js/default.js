function reloadCopyButton() {
	$('.copy-btn-wrapper').remove();

	var a = $('pre');
	var cnt = 0;
	for (var pre of a) {
		if (pre.textContent === '') continue;
		if (pre.id === '') {
			while ($('#copycode' + cnt).length !== 0) {
				cnt++;
			}
			pre.id = 'copycode' + cnt;
		}
	}
	for (pre of a) {
		if (pre.textContent === '') continue;
		var str = '<div class="copy-btn-wrapper">';
		str += '<button type="button" class="copy-btn" data-clipboard-target="#' + pre.id + '">Copy</button>';
		str += '</div>';
		$(pre).before(str);
	}

	var clipboard = new ClipboardJS('.copy-btn');
	clipboard.on('success', function (e) {
		e.clearSelection();
	});
	clipboard.on('error', function (e) {
		alert('Copy failed :(');
	});
}

function reloadHighlight() {
	document.querySelectorAll('pre code').forEach((block) => {
		if (!block.className.includes('language-in') && !block.className.includes('language-out')) {
			hljs.highlightBlock(block);
		}
	});
}

function reloadTableStyle() {
	$('table').addClass(['table-bordered', 'table-sm']);
}

function reloadIOStyle() {
	var a = $('code.language-in').parent();
	a.addClass('sample-in');
	a.prev().addClass('sample-in-wrapper');

	var b = $('code.language-out').parent();
	b.addClass('sample-out');
	b.prev().addClass('sample-out-wrapper');

	a.prev().before('<h6 class="d-sm-block d-md-none">Input</h6>');
	a.prev().before('<h6 class="d-none d-md-block" style="width:48%;float:left;">Input</h6>');
	a.prev().before('<h6 class="d-none d-md-block" style="width:48%;float:right;">Ouput</h6>');
	b.prev().before('<h6 class="d-sm-block d-md-none">Output</h6>');
	b.after('<div style="clear:both;margin-bottom:8px;"></div>');
}

function reloadMathJax() {
	MathJax.Hub.Config({
		tex2jax: {
			skipTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'],
			inlineMath: [
				['$', '$'],
				["\\(", "\\)"]
			],
			processEscapes: true
		}
	});
	MathJax.Hub.Queue(function () {
		var all = MathJax.Hub.getAllJax(),
			i;
		for (i = 0; i < all.length; i += 1) {
			all[i].SourceElement().parentNode.className += ' has-jax';
		}
	});
	MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
}

function reloadAll() {
	var postload = [reloadCopyButton, reloadTableStyle, reloadIOStyle];
	postload.forEach((fun) => {
		try {
			fun()
		} catch (err) {
			console.error(err);
		}
	});
}

function expandLang(data) {
	if (data[lang] !== undefined) {
		return data[lang];
	} else {
		for (var i of supportedLangs) {
			if (data[i] !== undefined) {
				return data[i];
			}
		}
	}
}

function reloadLangExpand() {
	$(".lang-expand").each(function () {
		const data = JSON.parse($(this).attr("data"));
		$(this).html(expandLang(data));
	});
}

function reloadMarkdown() {
	var converter = new showdown.Converter({
		'disableForced4SpacesIndentedSublists': true,
		'tasklists': true,
		'tables': true,
		'strikethrough': true,
		'prefixHeaderId': true,
		'extensions': ['mathjax', 'video', 'audio', 'catalog', 'anchor', 'youtube', 'bilibili'],
	});
	content = $("#content");
	if (!srcs.has(lang)) {
		content.html(`<p><b>Requested language "${lang}" doesn't exist!</b></p>`);
		return;
	}
	$.get(srcs.get(lang), function (data, status) {
		var text = data;
		html = converter.makeHtml(text);
		content.html(html);
		reloadAll();
	});
}

var supportedLangs = new Set(["zh", "en"]);
var lang = navigator.language.split('-')[0];

window.addEventListener('DOMContentLoaded', (event) => {
	var langParams = new URLSearchParams(location.search);
	if (!supportedLangs.has(lang)) {
		lang = "en";
	}
	if (typeof srcs !== 'undefined') {
		if (!srcs.has(lang)) {
			lang = srcs.keys().next().value;
		}
	}
	if (langParams.has('lang')) {
		lang = langParams.get('lang');
	}

	reloadLangExpand();
	if (typeof srcs !== 'undefined') {
		reloadMarkdown();
	}
});