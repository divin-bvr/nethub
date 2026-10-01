(function () {
  var el = document.getElementById("news-list");
  if (!el) return;

  function esc(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  fetch("/api/news")
    .then(function (r) {
      return r.json();
    })
    .then(function (rows) {
      if (!rows.length) {
        el.innerHTML = "<p>No headlines yet. Keep the lab server running so feeds can load.</p>";
        return;
      }
      el.innerHTML = rows
        .map(function (n) {
          return (
            '<article class="nh-card nh-news-item"><div class="nh-tag">' +
            esc(n.source) +
            "</div><h3><a href=\"" +
            esc(n.url) +
            '" target="_blank" rel="noopener">' +
            esc(n.title) +
            "</a></h3><p>" +
            esc(n.date) +
            "</p></article>"
          );
        })
        .join("");
    })
    .catch(function () {
      el.innerHTML = "<p>Start python server/app.py to fetch news.</p>";
    });
})();
