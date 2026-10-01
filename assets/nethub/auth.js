(function () {
  var API = "/api";

  function token() {
    return localStorage.getItem("nethub_token") || "";
  }

  window.nethubAuth = {
    token: token,
    setSession: function (data) {
      localStorage.setItem("nethub_token", data.token);
      localStorage.setItem("nethub_user", JSON.stringify(data.user));
    },
    clear: function () {
      localStorage.removeItem("nethub_token");
      localStorage.removeItem("nethub_user");
    },
    api: function (path, opts) {
      opts = opts || {};
      var headers = Object.assign({ "Content-Type": "application/json" }, opts.headers || {});
      if (token()) headers.Authorization = "Bearer " + token();
      return fetch(API + path, {
        method: opts.method || "GET",
        headers: headers,
        body: opts.body ? JSON.stringify(opts.body) : undefined
      }).then(function (res) {
        return res.text().then(function (text) {
          var data = {};
          try {
            data = text ? JSON.parse(text) : {};
          } catch (e) {
            throw new Error(res.ok ? "The desk did not return JSON." : "Desk request failed (" + res.status + ").");
          }
          if (!res.ok) throw new Error(data.error || "Request failed");
          return data;
        });
      });
    }
  };

  var params = new URLSearchParams(location.search);
  var sessionTok = params.get("session");
  if (sessionTok) {
    localStorage.setItem("nethub_token", sessionTok);
    fetch(API + "/me", { headers: { Authorization: "Bearer " + sessionTok } })
      .then(function (r) { return r.json(); })
      .then(function (user) {
        if (user && user.id) {
          localStorage.setItem("nethub_user", JSON.stringify(user));
          if (user.role === "admin") location.replace("admin.html");
          else location.replace(params.get("welcome") ? "dashboard.html?welcome=1" : "dashboard.html");
        }
      })
      .catch(function () {});
  }

  function afterLogin(data, requireAdmin) {
    if (requireAdmin && (!data.user || data.user.role !== "admin")) {
      nethubAuth.clear();
      throw new Error("This door is for the platform desk only.");
    }
    nethubAuth.setSession(data);
    if (data.just_registered) {
      location.href = "dashboard.html?welcome=1";
      return;
    }
    if (data.user && data.user.role === "admin") {
      location.href = "admin.html";
      return;
    }
    location.href = "dashboard.html";
  }

  document.querySelectorAll("[data-auth-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var err = form.querySelector(".nh-form-error");
      if (err) err.textContent = "";
      var payload = {};
      new FormData(form).forEach(function (value, key) {
        payload[key] = value;
      });
      var path = form.getAttribute("data-auth-form");
      var requireAdmin = form.getAttribute("data-require-admin") === "1";
      nethubAuth
        .api(path, { method: "POST", body: payload })
        .then(function (data) {
          afterLogin(data, requireAdmin);
        })
        .catch(function (ex) {
          if (err) err.textContent = ex.message;
        });
    });
  });

  var oauthHost = document.getElementById("nh-oauth");
  if (oauthHost) {
    fetch(API + "/auth/config")
      .then(function (r) { return r.json(); })
      .then(function (cfg) {
        var html = "";
        if (cfg.googleClientId) {
          html += '<div id="nh-google-btn"></div>';
        } else {
          html += '<p class="nh-oauth-note">Google sign-in: set <code>NETHUB_GOOGLE_CLIENT_ID</code> on the lab server (authorized origin http://127.0.0.1:8765), then restart Flask.</p>';
        }
        if (cfg.github) {
          html += '<a class="nh-oauth-btn" href="/api/auth/github">Continue with GitHub</a>';
        }
        oauthHost.innerHTML = html;
        if (!cfg.googleClientId) return;
        var s = document.createElement("script");
        s.src = "https://accounts.google.com/gsi/client";
        s.async = true;
        s.onload = function () {
          if (!window.google || !google.accounts || !google.accounts.id) return;
          google.accounts.id.initialize({
            client_id: cfg.googleClientId,
            callback: function (resp) {
              nethubAuth
                .api("/auth/google", { method: "POST", body: { credential: resp.credential } })
                .then(function (data) { afterLogin(data, false); })
                .catch(function (ex) {
                  var err = document.querySelector(".nh-form-error");
                  if (err) err.textContent = ex.message;
                });
            }
          });
          google.accounts.id.renderButton(document.getElementById("nh-google-btn"), {
            theme: "filled_black",
            size: "large",
            width: 360,
            text: "continue_with"
          });
        };
        document.head.appendChild(s);
      })
      .catch(function () {});
  }
})();
