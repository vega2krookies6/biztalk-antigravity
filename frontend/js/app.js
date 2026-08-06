document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const inputText = document.getElementById("inputText");
    const charCounter = document.getElementById("charCounter");
    const audienceCards = document.querySelectorAll(".audience-card");
    const convertBtn = document.getElementById("convertBtn");
    const outputText = document.getElementById("outputText");
    const outputPanel = document.getElementById("outputPanel");
    const skeletonOverlay = document.getElementById("skeletonOverlay");
    const copyBtn = document.getElementById("copyBtn");
    const toast = document.getElementById("toast");

    let selectedTarget = null;
    let isConverting = false;

    // Character Counter
    inputText.addEventListener("input", () => {
        const count = inputText.value.length;
        charCounter.textContent = `${count} / 1000자`;
    });

    // Audience Card Selection
    audienceCards.forEach(card => {
        card.addEventListener("click", () => {
            if (isConverting) return;

            // Remove active class from all cards
            audienceCards.forEach(c => c.classList.remove("active"));

            // Add active class to clicked card
            card.classList.add("active");
            selectedTarget = card.dataset.target;
        });
    });

    // Loading State Handler
    function setLoading(loading) {
        isConverting = loading;
        
        if (loading) {
            convertBtn.disabled = true;
            convertBtn.querySelector(".btn-text").textContent = "말투 변환 중...";
            outputPanel.classList.add("computing");
            skeletonOverlay.style.display = "flex";
            copyBtn.disabled = true;
            outputText.value = "";
        } else {
            convertBtn.disabled = false;
            convertBtn.querySelector(".btn-text").textContent = "말투 변환하기";
            outputPanel.classList.remove("computing");
            skeletonOverlay.style.display = "none";
        }
    }

    // Convert Tone Event
    convertBtn.addEventListener("click", async () => {
        const text = inputText.value.trim();

        if (!text) {
            alert("변환하고 싶은 원문을 입력해주세요.");
            inputText.focus();
            return;
        }

        if (!selectedTarget) {
            alert("수신 대상을 선택해주세요 (상사, 타팀 동료, 고객, 팀 내 동료).");
            return;
        }

        setLoading(true);

        try {
            // FastAPI backend 마운트 경로에 맞춘 상대 경로 호출
            const response = await fetch("/api/convert", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    text: text,
                    target_audience: selectedTarget
                })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || "서버 응답 오류가 발생했습니다.");
            }

            const data = await response.json();
            outputText.value = data.converted_text;
            copyBtn.disabled = false;

        } catch (error) {
            console.error("Conversion error:", error);
            outputText.value = `[오류 발생] 변환 중 문제가 발생했습니다.\n상세 사유: ${error.message}\n잠시 후 다시 시도해 주세요.`;
            copyBtn.disabled = true;
        } finally {
            setLoading(false);
        }
    });

    // Copy to Clipboard
    copyBtn.addEventListener("click", () => {
        const textToCopy = outputText.value;
        if (!textToCopy) return;

        navigator.clipboard.writeText(textToCopy)
            .then(() => {
                showToast();
            })
            .catch(err => {
                console.error("Copy failed:", err);
                alert("복사에 실패했습니다. 직접 복사해주세요.");
            });
    });

    // Toast Alert Show/Hide
    function showToast() {
        toast.classList.add("show");
        setTimeout(() => {
            toast.classList.remove("show");
        }, 2000);
    }
});
