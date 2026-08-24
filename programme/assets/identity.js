/* ==========================================================================
   Shared learner identity — name / cohort.

   Two jobs, both carried over unchanged in behaviour from the generated
   catalogue this site replaces:

   1. Store a name and cohort in this browser under `imls_identity`, and offer
      an intake form for setting them (present on the catalogue page only).
   2. Hand that identity to the modules through their launch URLs, and report
      launch analytics when — and only when — the page is served behind the
      IMLS collection server.

   Everything here is optional to the page working. If localStorage is blocked
   or absent, the intake reports that and every launch link stays exactly as it
   is written in the HTML.
   ========================================================================== */

(function () {
  "use strict";

  var KEY = "imls_identity";

  /* ---------------------------------------------------------------- store */

  function storageAvailable() {
    try {
      var probe = "__imls_store_test__";
      localStorage.setItem(probe, "1");
      localStorage.removeItem(probe);
      return true;
    } catch (e) {
      return false;
    }
  }

  var STORE_OK = storageAvailable();

  function read() {
    if (!STORE_OK) return {};
    try {
      var parsed = JSON.parse(localStorage.getItem(KEY) || "{}");
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch (e) {
      return {};
    }
  }

  function write(next) {
    if (!STORE_OK) return false;
    try {
      localStorage.setItem(KEY, JSON.stringify(next));
      return true;
    } catch (e) {
      /* quota, or storage blocked between the probe and now */
      return false;
    }
  }

  /* ------------------------------------------------------------- decorate */

  /* Hand the identity over in the URL as well as in localStorage.
     localStorage is per-ORIGIN: this site and the modules are on two different
     hosts (GitHub Pages and script.google.com), so it does not cross, and a
     learner would otherwise be asked again on arrival. The receiving client
     strips these parameters from the address bar the moment it reads them — a
     learner who copies the URL out of the bar into a group chat would otherwise
     be handing over their own name and cohort.

     Only `a.open` links — the modules themselves — are decorated. The
     analytics dashboards are an educator view and are left alone.

     The original href is stashed in `data-href` on first pass, and every later
     pass rebuilds from that stash rather than from the current href, so calling
     decorate() again after a save can never double-append. */
  function decorate() {
    var got = read();
    var links = document.querySelectorAll("a.open");
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var base = a.getAttribute("data-href") || a.getAttribute("href");
      if (!base) continue;
      a.setAttribute("data-href", base);

      var q = [];
      if (got.learner_id) q.push("imls_lid=" + encodeURIComponent(got.learner_id));
      if (got.learner_name) q.push("imls_ln=" + encodeURIComponent(got.learner_name));
      if (got.cohort) q.push("imls_ch=" + encodeURIComponent(got.cohort));

      if (!q.length) {
        a.setAttribute("href", base);
        continue;
      }
      var sep = base.indexOf("?") === -1 ? "?" : "&";
      a.setAttribute("href", base + sep + q.join("&"));
    }
  }

  /* ------------------------------------------------------------ analytics */

  /* A real navigation to a real target — the only honest link_opened in this
     system. window.IMLS exists only when the page is served by the collection
     server, which injects the shared sync client; as a plain file or on a
     static host these calls never fire. */
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("a.open") : null;
    if (!a || !window.IMLS || !window.IMLS.recordLearnerEvent) return;

    var host = a.closest("[data-id]");
    var moduleId = host ? host.getAttribute("data-id") : null;
    var title = host ? host.getAttribute("data-title") : null;

    window.IMLS.recordLearnerEvent("module_selected", {
      module_id: "lm", response: moduleId, section_name: title
    });
    window.IMLS.recordLearnerEvent("link_opened", {
      module_id: "lm", response: moduleId,
      section_name: a.getAttribute("data-href") || a.getAttribute("href")
    });
    window.IMLS.flushQueue();
  });

  /* --------------------------------------------------------------- intake */

  function initIntake() {
    var form = document.getElementById("intake");
    if (!form) return;

    var nameInput = document.getElementById("learnerName");
    var cohortInput = document.getElementById("learnerCohort");
    var statusEl = document.getElementById("intakeStatus");
    if (!nameInput || !cohortInput || !statusEl) return;

    var UNSET = "Not set. You can still open any module — each will ask for " +
      "your name when you get there.";

    function paint(identity) {
      var parts = [];
      if (identity && identity.learner_name) parts.push("Saved as " + identity.learner_name);
      if (identity && identity.cohort) parts.push("Cohort " + identity.cohort);

      statusEl.classList.remove("is-set", "is-warn");
      if (parts.length) {
        statusEl.textContent = parts.join(" · ") +
          ". This carries into the module links below.";
        statusEl.classList.add("is-set");
      } else {
        statusEl.textContent = UNSET;
      }
    }

    if (!STORE_OK) {
      statusEl.textContent = "This browser has storage turned off for this page, " +
        "so a name cannot be remembered here. Every module still opens normally.";
      statusEl.classList.add("is-warn");
      nameInput.disabled = true;
      cohortInput.disabled = true;
      var saveDisabled = document.getElementById("intakeSave");
      if (saveDisabled) saveDisabled.disabled = true;
      return;
    }

    var existing = read();
    nameInput.value = existing.learner_name || "";
    cohortInput.value = existing.cohort || "";
    paint(existing);

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      var name = nameInput.value.trim();
      var cohort = cohortInput.value.trim();

      /* Keep any learner_id a module may have written back into this record;
         this page never mints one itself. */
      var next = read();
      next.learner_name = name;
      next.cohort = cohort;

      if (!write(next)) {
        statusEl.textContent = "Could not save — this browser refused to store it. " +
          "Every module still opens normally.";
        statusEl.classList.remove("is-set");
        statusEl.classList.add("is-warn");
        return;
      }

      paint(next);
      decorate();
    });
  }

  /* ----------------------------------------------------------------- boot */

  decorate();
  initIntake();

  if (window.IMLS && window.IMLS.recordLearnerEvent) {
    window.IMLS.recordLearnerEvent("learning_material_opened", { module_id: "lm" });
  }
})();
