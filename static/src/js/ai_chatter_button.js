// ai_chatter_button.js
document.addEventListener("DOMContentLoaded", () => {
    const observer = new MutationObserver(() => {
        document.querySelectorAll("div.ms-1.flex-grow-1").forEach(container => {
            if (!container.querySelector(".ai-analyze-container")) {
                // Create container
                const wrapper = document.createElement("div");
                wrapper.className = "ai-analyze-container d-flex align-items-center";
                wrapper.style.gap = "6px";

                // Button
                const btn = document.createElement("button");
                btn.type = "button";
                btn.className = "btn btn-sm btn-info ai-analyze-btn";
                btn.innerText = "Analyze AI";

                // Append
                wrapper.appendChild(btn);
                container.appendChild(wrapper);

                btn.addEventListener("click", async (ev) => {
                    ev.stopPropagation(); // prevent Odoo from closing the chat
                    ev.preventDefault();


                    // Grab all message bodies from this chatter
                    const currentWindow = btn.closest(".o-mail-ChatWindow") || btn.closest(".o-mail-DiscussContent");
                    const threadId = currentWindow.dataset.threadId; // numeric ID
                    console.log(threadId);
                    const messages = Array.from(
                        currentWindow.querySelectorAll(".o-mail-Message-body p")
                    )
                        .map(p => p.innerText.trim())
                        .filter(text => text.length > 0)
                        .join("\n");

                    if (!messages) return alert("No messages to analyze");

                    btn.disabled = true;
                    btn.innerText = "Scanning AI...";
                    console.log(currentWindow);
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
                        console.log("AI response:", data);
                        const result = data.result || data;
                        // --- Create modal overlay ---
                        const modal = document.createElement("div");
                        modal.className = "ai-modal-overlay";
                        modal.innerHTML = `
                            <div class="ai-modal">
                                <h4>AI Analysis</h4>
                                <p><strong>Urgency:</strong><br>${result.urgency}</p>
                                <p><strong>Summary:</strong><br>${result.summary}</p>
                                <p><strong>Recommended Action:</strong>
                                <br>${result.recommendation}</p>
                                <button class="btn btn-sm btn-primary ai-close">Close</button>
                            </div>
                        `;
                        document.body.appendChild(modal);

                        // --- Close modal handlers ---
                        modal.querySelector(".ai-close").addEventListener("click", () => modal.remove());
                        modal.addEventListener("click", (e) => {
                            if (e.target === modal) modal.remove();
                        });
 
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
