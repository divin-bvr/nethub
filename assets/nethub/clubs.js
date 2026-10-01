(function () {
  function fillSelect(el, rows, valueKey, labelFn, placeholder) {
    if (!el) return;
    el.innerHTML = '<option value="">' + placeholder + "</option>";
    rows.forEach(function (row) {
      var opt = document.createElement("option");
      opt.value = row[valueKey];
      opt.textContent = labelFn(row);
      el.appendChild(opt);
    });
  }

  function bindSearchCombo(searchEl, hiddenEl, listEl, rows, onPick) {
    if (!searchEl || !hiddenEl || !listEl) return;
    function render(filter) {
      var q = (filter || "").toLowerCase();
      var match = rows.filter(function (r) {
        return !q || r.name.toLowerCase().indexOf(q) !== -1;
      });
      listEl.hidden = false;
      listEl.innerHTML = match
        .map(function (r) {
          return '<li role="option" data-id="' + r.id + '">' + r.name + "</li>";
        })
        .join("") || "<li>No match</li>";
    }
    searchEl.addEventListener("focus", function () {
      render(searchEl.value);
    });
    searchEl.addEventListener("input", function () {
      hiddenEl.value = "";
      render(searchEl.value);
    });
    listEl.addEventListener("click", function (e) {
      var li = e.target.closest("[data-id]");
      if (!li) return;
      hiddenEl.value = li.getAttribute("data-id");
      searchEl.value = li.textContent;
      listEl.hidden = true;
      if (onPick) onPick(hiddenEl.value);
    });
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".nh-combo")) listEl.hidden = true;
    });
  }

  function loadClubsForUniversity(id, clubSel) {
    if (!clubSel) return;
    if (!id) {
      clubSel.innerHTML = '<option value="">Search a university first</option>';
      return;
    }
    fetch("/api/clubs?university_id=" + encodeURIComponent(id))
      .then(function (r) { return r.json(); })
      .then(function (clubs) {
        fillSelect(clubSel, clubs, "id", function (c) {
          return c.name;
        }, clubs.length ? "Select a club" : "No club yet — create one");
      });
  }

  fetch("/api/universities")
    .then(function (r) { return r.json(); })
    .then(function (unis) {
      bindSearchCombo(
        document.getElementById("university-search"),
        document.getElementById("university-select"),
        document.getElementById("university-list"),
        unis,
        function (id) {
          loadClubsForUniversity(id, document.getElementById("club-select"));
        }
      );
      bindSearchCombo(
        document.getElementById("club-university-search"),
        document.getElementById("club-university"),
        document.getElementById("club-university-list"),
        unis
      );
    })
    .catch(function () {});

  var create = document.getElementById("club-create-form");
  if (create) {
    create.addEventListener("submit", function (e) {
      e.preventDefault();
      var err = create.querySelector(".nh-form-error");
      err.textContent = "";
      var payload = {};
      new FormData(create).forEach(function (v, k) {
        payload[k] = v;
      });
      if (!payload.university_id) {
        err.textContent = "Search and pick a university from the list.";
        return;
      }
      fetch("/api/clubs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })
        .then(function (r) {
          return r.json().then(function (data) {
            if (!r.ok) throw new Error(data.error || "Could not create the club");
            return data;
          });
        })
        .then(function () {
          location.href = "leaders.html";
        })
        .catch(function (ex) {
          err.textContent = ex.message;
        });
    });
  }

  var list = document.getElementById("term-leader-list");
  if (list) {
    fetch("/api/term-leaders")
      .then(function (r) { return r.json(); })
      .then(function (rows) {
        list.innerHTML = rows
          .map(function (r) {
            var tag = r.kind === "community" ? "Community" : r.university;
            return (
              '<article class="nh-card"><div class="nh-tag">' +
              tag +
              "</div><h3>" +
              r.name +
              "</h3><p>" +
              r.club +
              "<br>" +
              r.term +
              "</p></article>"
            );
          })
          .join("") || "<p>No term leaders posted yet.</p>";
      })
      .catch(function () {});
  }
})();
