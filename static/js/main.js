function showFeedback(answer) {
    const feedback = document.getElementById("feedback");
    feedback.style.display = "block";

    if (answer === "yes") {
        feedback.innerHTML = `
            <p><strong>Correct.</strong></p>
            <p>
                Repeated unwanted messages that cause distress may be considered online harassment.
                It is reasonable to take steps to protect yourself and seek support.
            </p>
        `;
    } else if (answer === "no") {
        feedback.innerHTML = `
            <p><strong>Not quite.</strong></p>
            <p>
                Even if messages seem minor, repeated unwanted contact after asking someone to stop
                can still be considered online abuse.
            </p>
        `;
    } else {
        feedback.innerHTML = `
            <p><strong>That’s understandable.</strong></p>
            <p>
                Many people are unsure. Learning how online abuse is defined can help you
                recognise situations and respond appropriately.
            </p>
        `;
    }
}
