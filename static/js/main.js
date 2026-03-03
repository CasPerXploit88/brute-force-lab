async function startCrack() {
    const password = document.getElementById("passwordInput").value.trim()
    const resultBox = document.getElementById("resultBox")
    const loader = document.getElementById("loader")
    const btn = document.getElementById("startBtn")

    if (!password) {
        alert("Please enter a password first")
        return
    }

    resultBox.style.display = "none"
    loader.style.display = "block"
    btn.disabled = true
    btn.textContent = "Cracking..."

    try {
        const response = await fetch("/crack", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password })
        })

        const data = await response.json()

        if (data.error) {
            alert(data.error)
            return
        }

        if (data.timeout) {
            document.getElementById("statusText").textContent = "⏱️ Timeout — Password Resisted Attack"
            document.getElementById("method").textContent = data.method
            document.getElementById("foundPassword").textContent = "Not cracked"
            document.getElementById("attempts").textContent = data.attempts.toLocaleString()
            document.getElementById("timeTaken").textContent = data.time_taken + "s"
            document.getElementById("strength").textContent = data.strength
        } else {
            document.getElementById("statusText").textContent = data.found ? "✅ Cracked" : "❌ Not Found"
            document.getElementById("method").textContent = data.method
            document.getElementById("foundPassword").textContent = data.found ? data.password : "—"
            document.getElementById("attempts").textContent = data.attempts.toLocaleString()
            document.getElementById("timeTaken").textContent = data.time_taken + "s"
            document.getElementById("strength").textContent = data.strength
        }

        resultBox.style.display = "flex"

    } catch (err) {
        alert("Something went wrong. Try again.")
    } finally {
        loader.style.display = "none"
        btn.disabled = false
        btn.textContent = "Start Attack"
    }
}