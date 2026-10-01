(function () {
  document.querySelectorAll("[data-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var err = form.querySelector(".nh-form-error");
      var ok = form.querySelector(".nh-form-ok");
      if (err) err.textContent = "";
      if (ok) ok.textContent = "";
      var payload = {};
      new FormData(form).forEach(function (v, k) {
        payload[k] = v;
      });
      fetch("/api/forms/" + form.getAttribute("data-form"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })
        .then(function (r) {
          return r.json().then(function (data) {
            if (!r.ok) throw new Error(data.error || "Could not save");
            return data;
          });
        })
        .then(function () {
          form.reset();
          if (ok) ok.textContent = "Saved in the Nethub desk database.";
        })
        .catch(function (ex) {
          if (err) err.textContent = ex.message;
        });
    });
  });
})();
