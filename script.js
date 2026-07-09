const button = document.querySelector("button");
const textarea = document.querySelector("textarea");
const output = document.querySelector(".output");

button.addEventListener("click", async () => {

    const idea = textarea.value.trim();

    if (!idea) {
        alert("Please enter a startup idea.");
        return;
    }

    output.innerHTML = `
        <h2>Generating Blueprint...</h2>
        <p>Please wait while IBM Granite generates your startup blueprint.</p>
    `;

    try {

        const response = await fetch("/generate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                idea: idea
            })

        });

        const data = await response.json();

        output.innerHTML = `
            <pre style="
                white-space: pre-wrap;
                font-size:16px;
                line-height:1.8;
                font-family: Arial;
            ">${data.result}</pre>
        `;

    }

    catch (error) {

        output.innerHTML = `
        <h2>Error</h2>
        <p>${error}</p>
        `;

    }

});