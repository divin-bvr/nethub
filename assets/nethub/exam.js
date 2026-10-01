(function () {
  var catsEl = document.getElementById("exam-cats");
  var homeErr = document.getElementById("exam-home-err");
  var runEl = document.getElementById("exam-run");
  var homeEl = document.getElementById("exam-home");
  var form = document.getElementById("exam-form");
  var scoreEl = document.getElementById("exam-score");
  var timerEl = document.getElementById("exam-timer");
  var submitBtn = document.getElementById("exam-submit");
  var retryBtn = document.getElementById("exam-retry");
  if (!catsEl || !form) return;

  var guestKey = localStorage.getItem("nethub_exam_guest") || "";
  var attempt = null;
  var tick = null;
  var locked = false;
  var activeSlug = "";

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function headers() {
    var h = { "Content-Type": "application/json" };
    var token = localStorage.getItem("nethub_token") || "";
    if (token) h.Authorization = "Bearer " + token;
    if (guestKey) h["X-Exam-Guest"] = guestKey;
    return h;
  }

  function api(path, body) {
    return fetch(path, {
      method: body ? "POST" : "GET",
      headers: headers(),
      body: body ? JSON.stringify(body) : undefined
    }).then(function (res) {
      return res.text().then(function (text) {
        var data = {};
        try {
          data = text ? JSON.parse(text) : {};
        } catch (e) {
          throw new Error("The desk did not return JSON.");
        }
        if (!res.ok) throw new Error(data.error || "Request failed");
        return data;
      });
    });
  }

  function tr(s) {
    return window.nethubPhrase ? window.nethubPhrase(s) : s;
  }

  function minsLabel(n) {
    return n + " min";
  }

  var catCache = [];

  function renderCats(rows) {
    if (rows) catCache = rows;
    catsEl.innerHTML = catCache
      .map(function (c) {
        return (
          '<button type="button" class="nh-course nh-exam-cat" data-slug="' +
          esc(c.slug) +
          '"><div class="nh-tag">' +
          esc(tr(c.difficulty)) +
          " · " +
          esc(minsLabel(c.minutes)) +
          "</div><h3>" +
          esc(tr(c.title)) +
          "</h3><p>" +
          esc(tr(c.blurb)) +
          '</p><span class="nh-tile-cta">' +
          esc(tr("20 questions")) +
          "</span></button>"
        );
      })
      .join("");
  }

  function qHtml(item, i) {
    var head =
      '<fieldset class="nh-card nh-exam-q" data-qid="' +
      esc(item.id) +
      '"><legend>' +
      (i + 1) +
      " / 20</legend><p>" +
      esc(item.q) +
      "</p>";
    if (item.type === "mcq") {
      return (
        head +
        item.choices
          .map(function (c, n) {
            return (
              '<label class="nh-exam-choice"><input type="radio" name="q-' +
              esc(item.id) +
              '" value="' +
              n +
              '"> ' +
              esc(c) +
              "</label>"
            );
          })
          .join("") +
        "</fieldset>"
      );
    }
    if (item.type === "fill") {
      return (
        head +
        '<input class="nh-exam-fill" name="q-' +
        esc(item.id) +
        '" autocomplete="off" placeholder="' +
        esc(tr("Short answer")) +
        '">' +
        "</fieldset>"
      );
    }
    var rights = item.right
      .map(function (r) {
        return '<option value="' + esc(r.id) + '">' + esc(r.text) + "</option>";
      })
      .join("");
    var rows = item.left
      .map(function (l) {
        return (
          '<div class="nh-exam-pair"><span>' +
          esc(l.text) +
          '</span><select name="q-' +
          esc(item.id) +
          "-" +
          esc(l.id) +
          '"><option value="">' +
          esc(tr("Match")) +
          "</option>" +
          rights +
          "</select></div>"
        );
      })
      .join("");
    return head + '<div class="nh-exam-match">' + rows + "</div></fieldset>";
  }

  function collect() {
    var answers = {};
    (attempt.questions || []).forEach(function (item) {
      if (item.type === "mcq") {
        var picked = form.querySelector('input[name="q-' + item.id + '"]:checked');
        if (picked) answers[item.id] = Number(picked.value);
      } else if (item.type === "fill") {
        var inp = form.querySelector('input[name="q-' + item.id + '"]');
        answers[item.id] = inp ? inp.value : "";
      } else {
        var map = {};
        (item.left || []).forEach(function (l) {
          var sel = form.querySelector('select[name="q-' + item.id + "-" + l.id + '"]');
          map[l.id] = sel ? sel.value : "";
        });
        answers[item.id] = map;
      }
    });
    return answers;
  }

  function stopTick() {
    if (tick) clearInterval(tick);
    tick = null;
  }

  function paintTimer() {
    if (!attempt || !attempt.ends_at) return;
    var left = Math.max(0, Date.parse(attempt.ends_at) - Date.now());
    var sec = Math.floor(left / 1000);
    var m = Math.floor(sec / 60);
    var s = sec % 60;
    timerEl.textContent = m + ":" + (s < 10 ? "0" : "") + s;
    if (left <= 0 && !locked) submitExam(true);
  }

  function showRun() {
    homeEl.hidden = true;
    runEl.hidden = false;
    runEl.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function showHome() {
    stopTick();
    locked = false;
    attempt = null;
    runEl.hidden = true;
    homeEl.hidden = false;
    submitBtn.hidden = false;
    retryBtn.hidden = true;
    scoreEl.textContent = "";
    form.innerHTML = "";
  }

  function startCategory(slug) {
    activeSlug = slug;
    homeErr.textContent = "";
    api("/api/exam/start", { category: slug, guest_key: guestKey })
      .then(function (data) {
        if (data.guest_key) {
          guestKey = data.guest_key;
          localStorage.setItem("nethub_exam_guest", guestKey);
        }
        attempt = data;
        locked = false;
        document.getElementById("exam-cat-title").textContent = tr(data.category.title);
        document.getElementById("exam-diff").textContent =
          tr(data.category.difficulty) + " · " + data.minutes + " min · " + tr("20 questions");
        form.innerHTML = data.questions.map(qHtml).join("");
        scoreEl.textContent = "Each new attempt shuffles the order and swaps about 30% of the questions.";
        submitBtn.hidden = false;
        submitBtn.disabled = false;
        retryBtn.hidden = true;
        showRun();
        stopTick();
        paintTimer();
        tick = setInterval(paintTimer, 500);
      })
      .catch(function (ex) {
        homeErr.textContent = ex.message || String(ex);
      });
  }

  function markDetail(detail) {
    (detail || []).forEach(function (row) {
      var box = form.querySelector('[data-qid="' + row.id + '"]');
      if (!box) return;
      box.classList.toggle("is-wrong", !row.ok);
      box.classList.toggle("is-right", !!row.ok);
    });
  }

  function submitExam(fromTimer) {
    if (!attempt || locked) return;
    locked = true;
    stopTick();
    submitBtn.disabled = true;
    api("/api/exam/submit", {
      attempt_id: attempt.attempt_id,
      guest_key: guestKey,
      answers: collect()
    })
      .then(function (data) {
        var extra = fromTimer ? " Time is up. " : " ";
        scoreEl.textContent =
          extra +
          data.score +
          " / " +
          data.total +
          " correct. Take another attempt — about 30% of the set will be new, and the rest will shuffle.";
        markDetail(data.detail);
        retryBtn.hidden = false;
        form.querySelectorAll("input, select").forEach(function (el) {
          el.disabled = true;
        });
      })
      .catch(function (ex) {
        locked = false;
        submitBtn.disabled = false;
        scoreEl.textContent = ex.message || String(ex);
      });
  }

  catsEl.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-slug]");
    if (btn) startCategory(btn.getAttribute("data-slug"));
  });

  document.getElementById("exam-back").addEventListener("click", showHome);
  submitBtn.addEventListener("click", function () {
    submitExam(false);
  });
  retryBtn.addEventListener("click", function () {
    startCategory(activeSlug);
  });

  api("/api/exam/categories")
    .then(renderCats)
    .catch(function () {
      homeErr.textContent = tr("Start the lab server so the category cards can load.");
    });

  document.addEventListener("nethub:lang", function () {
    renderCats();
    var back = document.getElementById("exam-back");
    if (back) back.textContent = tr("Categories");
    if (submitBtn) submitBtn.textContent = tr("Submit answers");
    if (retryBtn) retryBtn.textContent = tr("New attempt");
  });
})();
