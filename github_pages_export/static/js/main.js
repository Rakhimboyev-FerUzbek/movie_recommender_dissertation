console.log("Movie Recommender UI initialized.");
document.addEventListener("DOMContentLoaded", () => {
    const modal = document.querySelector("[data-delete-modal]");
    const backdrop = document.querySelector("[data-delete-modal-backdrop]");
    const openBtn = document.querySelector("[data-delete-modal-open]");
    const closeButtons = document.querySelectorAll("[data-delete-modal-close]");

    if (!modal || !backdrop || !openBtn) return;

    const openModal = () => {
        modal.hidden = false;
        backdrop.hidden = false;
        requestAnimationFrame(() => {
            modal.classList.add("is-active");
            backdrop.classList.add("is-active");
        });
        modal.setAttribute("aria-hidden", "false");
        document.body.classList.add("modal-open");
    };

    const closeModal = () => {
        modal.classList.remove("is-active");
        backdrop.classList.remove("is-active");
        modal.setAttribute("aria-hidden", "true");
        document.body.classList.remove("modal-open");
        setTimeout(() => {
            modal.hidden = true;
            backdrop.hidden = true;
        }, 230);
    };

    openBtn.addEventListener("click", openModal);

    closeButtons.forEach((btn) => {
        btn.addEventListener("click", closeModal);
    });

    backdrop.addEventListener("click", closeModal);

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !modal.hidden) {
            closeModal();
        }
    });
});

console.log("Movie Recommender UI initialized.");

document.addEventListener("DOMContentLoaded", () => {
    initInteractionSortSelects();
});

function initInteractionSortSelects() {
    const selects = document.querySelectorAll(
        ".interaction-filter-form select.interaction-sort-native"
    );

    selects.forEach((select) => {
        if (select.dataset.enhanced === "1") {
            return;
        }

        select.dataset.enhanced = "1";
        select.classList.add("is-enhanced-select");

        const wrapper = document.createElement("div");
        wrapper.className = "catalog-ui-select interaction-ui-select";

        const trigger = document.createElement("button");
        trigger.type = "button";
        trigger.className = "catalog-ui-select__trigger";
        trigger.setAttribute("aria-haspopup", "listbox");
        trigger.setAttribute("aria-expanded", "false");

        const triggerText = document.createElement("span");
        triggerText.className = "catalog-ui-select__value";

        const triggerChevron = document.createElement("span");
        triggerChevron.className = "catalog-ui-select__chevron";

        trigger.appendChild(triggerText);
        trigger.appendChild(triggerChevron);

        const menu = document.createElement("div");
        menu.className = "catalog-ui-select__menu";
        menu.setAttribute("role", "listbox");

        Array.from(select.options).forEach((option) => {
            const optionBtn = document.createElement("button");
            optionBtn.type = "button";
            optionBtn.className = "catalog-ui-select__option";
            optionBtn.textContent = option.textContent;
            optionBtn.dataset.value = option.value;
            optionBtn.setAttribute("role", "option");

            if (option.value === select.value) {
                optionBtn.classList.add("is-active");
            }

            optionBtn.addEventListener("click", () => {
                select.value = option.value;
                syncSelectUi(select, triggerText, menu);
                closeSelect(wrapper, trigger);
                select.dispatchEvent(new Event("change", { bubbles: true }));
            });

            menu.appendChild(optionBtn);
        });

        select.parentNode.insertBefore(wrapper, select);
        wrapper.appendChild(select);
        wrapper.appendChild(trigger);
        wrapper.appendChild(menu);

        syncSelectUi(select, triggerText, menu);

        trigger.addEventListener("click", (event) => {
            event.preventDefault();
            const isOpen = wrapper.classList.contains("is-open");
            closeAllInteractionSelects();
            if (!isOpen) {
                openSelect(wrapper, trigger);
            }
        });

        document.addEventListener("click", (event) => {
            if (!wrapper.contains(event.target)) {
                closeSelect(wrapper, trigger);
            }
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                closeSelect(wrapper, trigger);
            }
        });

        select.addEventListener("change", () => {
            syncSelectUi(select, triggerText, menu);
        });
    });
}

function syncSelectUi(select, triggerText, menu) {
    const selectedOption = select.options[select.selectedIndex];
    triggerText.textContent = selectedOption ? selectedOption.textContent : "Tanlang";

    menu.querySelectorAll(".catalog-ui-select__option").forEach((btn) => {
        btn.classList.toggle("is-active", btn.dataset.value === select.value);
    });
}

function openSelect(wrapper, trigger) {
    wrapper.classList.add("is-open");
    trigger.setAttribute("aria-expanded", "true");
}

function closeSelect(wrapper, trigger) {
    wrapper.classList.remove("is-open");
    trigger.setAttribute("aria-expanded", "false");
}

function closeAllInteractionSelects() {
    document.querySelectorAll(".interaction-ui-select.is-open").forEach((wrapper) => {
        wrapper.classList.remove("is-open");
        const trigger = wrapper.querySelector(".catalog-ui-select__trigger");
        if (trigger) {
            trigger.setAttribute("aria-expanded", "false");
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.querySelector("[data-delete-modal]");
    const backdrop = document.querySelector("[data-delete-modal-backdrop]");
    const openBtn = document.querySelector("[data-delete-modal-open]");
    const closeButtons = document.querySelectorAll("[data-delete-modal-close]");

    if (!modal || !backdrop || !openBtn) return;

    function openModal() {
        modal.hidden = false;
        backdrop.hidden = false;
        requestAnimationFrame(function() {
            modal.classList.add("is-active");
            backdrop.classList.add("is-active");
        });
        modal.setAttribute("aria-hidden", "false");
        document.body.classList.add("modal-open");
    }

    function closeModal() {
        modal.classList.remove("is-active");
        backdrop.classList.remove("is-active");
        modal.setAttribute("aria-hidden", "true");
        document.body.classList.remove("modal-open");
        setTimeout(function() {
            modal.hidden = true;
            backdrop.hidden = true;
        }, 230);
    }

    openBtn.addEventListener("click", openModal);

    closeButtons.forEach(function (btn) {
        btn.addEventListener("click", closeModal);
    });

    backdrop.addEventListener("click", closeModal);

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && !modal.hidden) {
            closeModal();
        }
    });
});

console.log("Movie Recommender UI initialized.");

document.addEventListener("DOMContentLoaded", () => {
    initInteractionSortSelects();
    initInteractionRealtimeSearch();
    initReviewToggles();
});

function initInteractionSortSelects() {
    const selects = document.querySelectorAll(
        ".interaction-filter-form select.interaction-sort-native"
    );

    selects.forEach((select) => {
        if (select.dataset.enhanced === "1") return;

        select.dataset.enhanced = "1";
        select.classList.add("is-enhanced-select");

        const wrapper = document.createElement("div");
        wrapper.className = "catalog-ui-select interaction-ui-select";

        const trigger = document.createElement("button");
        trigger.type = "button";
        trigger.className = "catalog-ui-select__trigger";
        trigger.setAttribute("aria-haspopup", "listbox");
        trigger.setAttribute("aria-expanded", "false");

        const triggerText = document.createElement("span");
        triggerText.className = "catalog-ui-select__value";

        const triggerChevron = document.createElement("span");
        triggerChevron.className = "catalog-ui-select__chevron";

        trigger.appendChild(triggerText);
        trigger.appendChild(triggerChevron);

        const menu = document.createElement("div");
        menu.className = "catalog-ui-select__menu";
        menu.setAttribute("role", "listbox");

        Array.from(select.options).forEach((option) => {
            const optionBtn = document.createElement("button");
            optionBtn.type = "button";
            optionBtn.className = "catalog-ui-select__option";
            optionBtn.textContent = option.textContent;
            optionBtn.dataset.value = option.value;
            optionBtn.setAttribute("role", "option");

            if (option.value === select.value) {
                optionBtn.classList.add("is-active");
            }

            optionBtn.addEventListener("click", () => {
                select.value = option.value;
                syncSelectUi(select, triggerText, menu);
                closeSelect(wrapper, trigger);

                // sort o'zgarsa darrov form submit
                const form = select.closest("form");
                if (form) {
                    form.submit();
                }
            });

            menu.appendChild(optionBtn);
        });

        select.parentNode.insertBefore(wrapper, select);
        wrapper.appendChild(select);
        wrapper.appendChild(trigger);
        wrapper.appendChild(menu);

        syncSelectUi(select, triggerText, menu);

        trigger.addEventListener("click", (event) => {
            event.preventDefault();
            const isOpen = wrapper.classList.contains("is-open");
            closeAllInteractionSelects();
            if (!isOpen) {
                openSelect(wrapper, trigger);
            }
        });

        document.addEventListener("click", (event) => {
            if (!wrapper.contains(event.target)) {
                closeSelect(wrapper, trigger);
            }
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                closeSelect(wrapper, trigger);
            }
        });

        select.addEventListener("change", () => {
            syncSelectUi(select, triggerText, menu);
        });
    });
}

function syncSelectUi(select, triggerText, menu) {
    const selectedOption = select.options[select.selectedIndex];
    triggerText.textContent = selectedOption ? selectedOption.textContent : "Tanlang";

    menu.querySelectorAll(".catalog-ui-select__option").forEach((btn) => {
        btn.classList.toggle("is-active", btn.dataset.value === select.value);
    });
}

function openSelect(wrapper, trigger) {
    wrapper.classList.add("is-open");
    trigger.setAttribute("aria-expanded", "true");
}

function closeSelect(wrapper, trigger) {
    wrapper.classList.remove("is-open");
    trigger.setAttribute("aria-expanded", "false");
}

function closeAllInteractionSelects() {
    document.querySelectorAll(".interaction-ui-select.is-open").forEach((wrapper) => {
        wrapper.classList.remove("is-open");
        const trigger = wrapper.querySelector(".catalog-ui-select__trigger");
        if (trigger) {
            trigger.setAttribute("aria-expanded", "false");
        }
    });
}

/* =========================
   INTERACTIONS REALTIME SEARCH
   ratings / favorites / watch-history
   ========================= */
function initInteractionRealtimeSearch() {
    const forms = document.querySelectorAll(".interaction-filter-form");

    forms.forEach((form) => {
        const searchInput = form.querySelector('input[name="q"]');
        if (!searchInput) return;

        if (!searchInput.dataset.realtimeBound) {
            searchInput.dataset.realtimeBound = "1";
            searchInput.classList.add("interaction-realtime-search");

            if (!searchInput.parentElement.classList.contains("interaction-search-wrap")) {
                const wrap = document.createElement("div");
                wrap.className = "interaction-search-wrap";

                searchInput.parentNode.insertBefore(wrap, searchInput);
                wrap.appendChild(searchInput);

                const spinner = document.createElement("span");
                spinner.className = "interaction-search-spinner";
                wrap.appendChild(spinner);
            }
        }

        let debounceTimer = null;
        let activeController = null;

        const loadResults = async () => {
            const wrap = searchInput.closest(".interaction-search-wrap");
            const resultsContainer = document.getElementById("interactionResults");
            if (!resultsContainer) return;

            const formData = new FormData(form);
            formData.delete("page");

            const params = new URLSearchParams();
            for (const [key, value] of formData.entries()) {
                if (value !== "") {
                    params.append(key, value);
                }
            }

            const url = `${window.location.pathname}?${params.toString()}`;

            if (activeController) {
                activeController.abort();
            }

            activeController = new AbortController();

            if (wrap) {
                wrap.classList.add("is-searching");
            }

            try {
                const response = await fetch(url, {
                    method: "GET",
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                    },
                    signal: activeController.signal,
                });

                if (!response.ok) return;

                const html = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, "text/html");
                const newResults = doc.getElementById("interactionResults");

                if (newResults) {
                    resultsContainer.innerHTML = newResults.innerHTML;
                    window.history.replaceState({}, "", url);
                    bindInteractionPagination();
                }
            } catch (error) {
                if (error.name !== "AbortError") {
                    console.error("Realtime search error:", error);
                }
            } finally {
                if (wrap) {
                    wrap.classList.remove("is-searching");
                }
            }
        };

        searchInput.addEventListener("input", () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(loadResults, 400);
        });

        searchInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                clearTimeout(debounceTimer);
                loadResults();
            }
        });
    });

    bindInteractionPagination();
}
function bindInteractionPagination() {
    const resultsContainer = document.getElementById("interactionResults");
    if (!resultsContainer || resultsContainer.dataset.paginationBound === "1") {
        return;
    }

    resultsContainer.dataset.paginationBound = "1";

    resultsContainer.addEventListener("click", async (event) => {
        const link = event.target.closest(".pagination-compact-link[href]");
        if (!link) return;

        event.preventDefault();

        try {
            const response = await fetch(link.href, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            });

            if (!response.ok) return;

            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, "text/html");
            const newResults = doc.getElementById("interactionResults");

            if (newResults) {
                resultsContainer.innerHTML = newResults.innerHTML;
                window.history.replaceState({}, "", link.href);
                resultsContainer.dataset.paginationBound = "0";
                bindInteractionPagination();
            }
        } catch (error) {
            console.error("Pagination load error:", error);
        }
    });
}

function initReviewToggles() {
    document.addEventListener("click", (event) => {
        const button = event.target.closest(".interaction-review-toggle");
        if (!button) return;

        const targetId = button.dataset.target;
        const reviewBox = document.getElementById(targetId);
        if (!reviewBox) return;

        const isCollapsed = reviewBox.classList.contains("is-collapsed");

        if (isCollapsed) {
            reviewBox.classList.remove("is-collapsed");
            button.textContent = "Yashirish";
            button.setAttribute("aria-expanded", "true");
        } else {
            reviewBox.classList.add("is-collapsed");
            button.textContent = "Ko‘proq";
            button.setAttribute("aria-expanded", "false");
        }
    });
}