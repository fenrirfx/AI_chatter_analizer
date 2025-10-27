// ai_chatter_button.js
document.addEventListener("DOMContentLoaded", () => {
    const observer = new MutationObserver(() => {
        document.querySelectorAll("div.ms-1.flex-grow-1").forEach(container => {
            if (!container.querySelector(".ai-analyze-btn")) {
                const btn = document.createElement("button");
                btn.type = "button";
                btn.className = "btn btn-sm btn-info ai-analyze-btn ml-2";
                btn.innerHTML = "⭐ AI Scan"; // star + text
                container.appendChild(btn);

                btn.addEventListener("click", async (ev) => {
                    ev.stopPropagation(); // prevent Odoo from closing the chat
                    ev.preventDefault();

                    // Grab all message bodies from this chatter
                    const messages = Array.from(
                        btn.closest(".o-mail-ChatWindow")
                        .querySelectorAll(".o-mail-Message-body p")
                    )
                        .map(p => p.innerText.trim())
                        .filter(text => text.length > 0)
                        .join("\n");

                    if (!messages) return alert("No messages to analyze");

                    btn.disabled = true;
                    btn.innerText = "Scanning AI...";

                    try {
                        const response = await fetch("/ai_chatter/scan", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "X-Requested-With": "XMLHttpRequest",
                            },
                            body: JSON.stringify({ messages }),
                        });

                        const data = await response.json();

                        // --- Create modal overlay ---
                        const modal = document.createElement("div");
                        modal.className = "ai-modal-overlay";
                        modal.innerHTML = `
                            <div class="ai-modal">
                                <h4>AI Analysis</h4>
                                <p><strong>Summary:</strong><br>${data.summary || "No summary"}</p>
                                <button class="btn btn-sm btn-primary ai-close">Close</button>
                            </div>
                        `;
                        document.body.appendChild(modal);

                        // --- Close modal handlers ---
                        modal.querySelector(".ai-close").addEventListener("click", () => modal.remove());
                        modal.addEventListener("click", (e) => {
                            if (e.target === modal) modal.remove();
                        });

                        // --- Insert text into composer ---
                        // const chatWindow = btn.closest(".o-mail-ChatWindow");
                        // const composer = chatWindow.querySelector(".o-mail-Composer-input");
                        // const sendBtn = chatWindow.querySelector("button[name='send-message']");

                        // if (composer && sendBtn) {
                        //     // Set the text in the composer
                        //     composer.value = "Hello AI suggestion";
                        //     composer.dispatchEvent(new Event('input', { bubbles: true })); // trigger OWL reactivity

                        //     // Trigger a proper OWL-compatible click
                        //     const clickEvent = new MouseEvent('click', {
                        //         view: window,
                        //         bubbles: true,
                        //         cancelable: true
                        //     });
                        //     sendBtn.dispatchEvent(clickEvent);
                        // }
 
                    } catch (err) {
                        console.error(err);
                        alert(err);
                    } finally {
                        btn.disabled = false;
                        btn.innerText = "★ AI Scan";
                    }
                });

            }
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
});
