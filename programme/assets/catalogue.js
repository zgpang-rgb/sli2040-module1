/* ==========================================================================
   Catalogue controls — outcome search, module filter, expand / collapse.

   The generated page this site replaces promised "Search the outcomes to find
   which module carries a topic" but shipped only a module dropdown; its search
   input, <mark> highlighting and empty state were styled but never rendered.
   This is that search, built against the same markup.

   The outcome text each card is searched on is captured once, at start-up,
   from the list items themselves — there is no parallel copy of the text in a
   data attribute to fall out of step with what the page actually shows.
   ========================================================================== */

(function () {
  "use strict";

  var searchInput = document.getElementById("q");
  var moduleSel = document.getElementById("m");
  var expandBtn = document.getElementById("expand");
  var clearBtn = document.getElementById("clear");
  var hits = document.getElementById("hits");
  var empty = document.getElementById("empty");
  if (!searchInput || !moduleSel || !expandBtn || !clearBtn || !hits || !empty) return;

  var leaves = Array.prototype.slice.call(document.querySelectorAll(".leaf"))
    .map(function (leaf) {
      var items = Array.prototype.slice.call(leaf.querySelectorAll("ol.outcomes li"))
        .map(function (li) {
          return { li: li, plain: li.textContent.replace(/\s+/g, " ").trim() };
        });
      var heading = leaf.querySelector(".leafhead h2");
      return {
        el: leaf,
        id: leaf.getAttribute("data-id"),
        items: items,
        title: { li: heading, plain: heading.textContent.replace(/\s+/g, " ").trim() },
        body: leaf.querySelector(".body"),
        head: leaf.querySelector(".leafhead"),
        chev: leaf.querySelector(".chev")
      };
    });

  /* ------------------------------------------------------------ highlight */

  /* Rebuilt as text and <mark> nodes from the captured plain string, never by
     assigning innerHTML — the needle comes straight from a text field.
     `target` is any {node, plain} pair: an outcome, or a card heading. */
  function paintMatches(target, needle) {
    var node = target.li;
    while (node.firstChild) node.removeChild(node.firstChild);

    if (!needle) {
      node.appendChild(document.createTextNode(target.plain));
      return;
    }

    var haystack = target.plain.toLowerCase();
    var from = 0;
    var at = haystack.indexOf(needle, from);

    while (at !== -1) {
      if (at > from) {
        node.appendChild(document.createTextNode(target.plain.slice(from, at)));
      }
      var mark = document.createElement("mark");
      mark.appendChild(document.createTextNode(target.plain.slice(at, at + needle.length)));
      node.appendChild(mark);
      from = at + needle.length;
      at = haystack.indexOf(needle, from);
    }
    if (from < target.plain.length) {
      node.appendChild(document.createTextNode(target.plain.slice(from)));
    }
  }

  /* ----------------------------------------------------------- open/close */

  function open(leaf, state) {
    leaf.body.hidden = !state;
    leaf.head.setAttribute("aria-expanded", String(state));
    leaf.chev.textContent = state ? "Hide" : "Show";
  }

  function syncExpandLabel() {
    var anyClosed = leaves.some(function (l) { return !l.el.hidden && l.body.hidden; });
    expandBtn.textContent = anyClosed ? "Expand all" : "Collapse all";
  }

  /* --------------------------------------------------------------- filter */

  function apply() {
    var needle = searchInput.value.trim().toLowerCase();
    var only = moduleSel.value;
    var shownModules = 0;
    var shownOutcomes = 0;

    leaves.forEach(function (leaf) {
      var inScope = !only || leaf.id === only;

      /* The module's own title counts as a match. Without this, searching
         "methodolog" would not surface a3 — the module actually called Research
         Methodologies — because none of its seven outcomes happen to use the
         word. A title hit keeps the whole card, since there is nothing to
         narrow it down to. */
      var titleHit = !!needle && leaf.title.plain.toLowerCase().indexOf(needle) !== -1;
      paintMatches(leaf.title, needle);

      var matched = 0;
      leaf.items.forEach(function (item) {
        if (item.plain.toLowerCase().indexOf(needle) !== -1) matched++;
      });

      var showAll = !needle || (titleHit && matched === 0);
      leaf.items.forEach(function (item) {
        var isHit = showAll || item.plain.toLowerCase().indexOf(needle) !== -1;
        item.li.hidden = !isHit;
        paintMatches(item, isHit && !showAll ? needle : "");
      });

      /* With a search running, a module matching on neither its title nor any
         outcome drops out entirely — that is what makes the search a way of
         finding which module carries a topic. */
      var visible = inScope && (!needle || titleHit || matched > 0);
      leaf.el.hidden = !visible;

      if (visible) {
        shownModules++;
        shownOutcomes += showAll ? leaf.items.length : matched;
        /* Open on a search so the hits are actually on screen; a search whose
           results stayed collapsed would be hiding its own answer. */
        if (needle) open(leaf, true);
      }
    });

    hits.textContent = needle
      ? shownModules + " module(s), " + shownOutcomes + " learning outcome(s) shown"
      : shownModules + " module(s), " + shownOutcomes + " learning outcomes";
    empty.hidden = shownModules > 0;
    syncExpandLabel();
  }

  /* --------------------------------------------------------------- events */

  leaves.forEach(function (leaf) {
    leaf.head.addEventListener("click", function () {
      open(leaf, leaf.body.hidden);
      syncExpandLabel();
    });
  });

  expandBtn.addEventListener("click", function () {
    var anyClosed = leaves.some(function (l) { return !l.el.hidden && l.body.hidden; });
    leaves.forEach(function (l) { if (!l.el.hidden) open(l, anyClosed); });
    syncExpandLabel();
  });

  searchInput.addEventListener("input", apply);
  moduleSel.addEventListener("change", apply);

  clearBtn.addEventListener("click", function () {
    searchInput.value = "";
    moduleSel.value = "";
    apply();
    leaves.forEach(function (l) { open(l, false); });
    syncExpandLabel();
    searchInput.focus();
  });

  leaves.forEach(function (l) { open(l, false); });
  apply();
})();
