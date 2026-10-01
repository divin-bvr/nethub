(function () {
  if (!nethubAuth.token()) {
    location.href = "login.html";
    return;
  }

  var modal = document.getElementById("welcome-modal");
  if (new URLSearchParams(location.search).get("welcome") === "1" && modal) {
    modal.hidden = false;
  }
  var ok = document.getElementById("welcome-ok");
  if (ok) {
    ok.addEventListener("click", function () {
      modal.hidden = true;
      history.replaceState({}, "", "dashboard.html");
    });
  }

  var logoutBtn = document.getElementById("nh-logout");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", function (e) {
      e.preventDefault();
      nethubAuth.clear();
      location.href = "index.html";
    });
  }

  function renderRequests(el, rows, labelKey) {
    if (!rows.length) {
      el.innerHTML = "<li>None yet.</li>";
      return;
    }
    el.innerHTML = rows
      .map(function (r) {
        return "<li><strong>" + escapeHtml(r[labelKey]) + "</strong> · " + escapeHtml(r.status) + "<br><span>" + escapeHtml(r.created_at) + "</span></li>";
      })
      .join("");
  }

  function escapeHtml(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/"/g, "&quot;");
  }

  function loadMe() {
    return nethubAuth.api("/me").then(function (data) {
      var u = data.user;
      document.getElementById("dash-hello").textContent = "Hello, " + u.name.split(" ")[0];
      var status = document.getElementById("dash-status");
      if (u.status === "pending") {
        status.textContent = "Profile is in verification. The desk will approve this seat. You can still use the room below.";
      } else if (u.status === "approved") {
        status.textContent = (u.campus ? u.campus + " · " : "") + "Seat approved. Request Zoom, watch, pick a path.";
      } else {
        status.textContent = "This seat is not open. Write the desk.";
      }
      document.getElementById("dash-kicker").textContent =
        u.role === "admin" ? "Admin" : u.role === "mentor" ? "Mentor" : "Student";
      renderRequests(document.getElementById("mentor-list"), data.mentor_requests, "topic");
      renderRequests(document.getElementById("career-list"), data.career_requests, "goal");
      return data;
    });
  }

  function loadVideos() {
    return nethubAuth.api("/videos").then(function (rows) {
      document.getElementById("video-list").innerHTML = rows
        .map(function (v) {
          return (
            '<article class="nh-card nh-video-card">' +
            '<div class="nh-tag">' + escapeHtml(v.field) + "</div>" +
            '<div class="nh-video-frame"><iframe src="https://www.youtube-nocookie.com/embed/' +
            encodeURIComponent(v.youtube_id) +
            '" title="' +
            escapeHtml(v.title) +
            '" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>' +
            "<h3>" +
            escapeHtml(v.title) +
            "</h3><p>" +
            escapeHtml(v.duration) +
            "</p></article>"
          );
        })
        .join("");
    });
  }

  var pickedIds = {};

  function loadRoadmaps() {
    return nethubAuth.api("/roadmaps").then(function (rows) {
      document.getElementById("roadmap-list").innerHTML = rows
        .map(function (r) {
          var steps = (r.steps || [])
            .map(function (s) {
              return "<li>" + escapeHtml(s) + "</li>";
            })
            .join("");
          var on = pickedIds[r.id] ? " is-picked" : "";
          return (
            '<article class="nh-card nh-roadmap' +
            on +
            '"><div class="nh-tag">' +
            escapeHtml(r.field) +
            "</div><h3>" +
            escapeHtml(r.title) +
            "</h3><p>" +
            escapeHtml(r.summary) +
            "</p><ol>" +
            steps +
            '</ol><button class="nh-btn nh-btn-primary" type="button" data-pick="' +
            r.id +
            '">' +
            (pickedIds[r.id] ? "Picked" : "Pick this path") +
            "</button></article>"
          );
        })
        .join("");
    });
  }

  document.getElementById("roadmap-list").addEventListener("click", function (e) {
    var btn = e.target.closest("[data-pick]");
    if (!btn) return;
    var id = btn.getAttribute("data-pick");
    nethubAuth.api("/roadmaps/" + id + "/pick", { method: "POST" }).then(function () {
      pickedIds[id] = true;
      return loadRoadmaps();
    });
  });

  function bindForm(id, path) {
    var form = document.getElementById(id);
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var err = form.querySelector(".nh-form-error");
      err.textContent = "";
      var payload = {};
      new FormData(form).forEach(function (v, k) {
        payload[k] = v;
      });
      nethubAuth
        .api(path, { method: "POST", body: payload })
        .then(function () {
          form.reset();
          return loadMe();
        })
        .catch(function (ex) {
          err.textContent = ex.message;
        });
    });
  }

  bindForm("mentor-form", "/mentor-requests");
  bindForm("career-form", "/career-requests");

  loadMe()
    .then(function (data) {
      (data.roadmaps || []).forEach(function (r) {
        pickedIds[r.id] = true;
      });
      return Promise.all([loadVideos(), loadRoadmaps()]);
    })
    .catch(function () {
      nethubAuth.clear();
      location.href = "login.html";
    });
})();
