const form = document.getElementById("rform");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formdata = new FormData(form)

    try {
        const response = await fetch("/addReview", {
            method: "POST",
            body: formdata
        });
        const data = await response.json();

        const key = Object.keys(data);

        if (key[0] === 'user') {
            // create new div and add the response to it
            const parentDiv = document.getElementById("reviewDiv");
            const childDiv = document.createElement('div');
            childDiv.className = "mb-3";

            const sh = document.createElement("strong");
            sh.textContent = data.user;
            const h4 = document.createElement('h4');
            h4.appendChild(sh);
            const p = document.createElement('p');
            p.textContent = data.content;

            const hr = document.createElement("hr");
            childDiv.appendChild(h4);
            childDiv.appendChild(p);
            childDiv.appendChild(hr);

            parentDiv.prepend(childDiv);

        }
        if (key[0] == "err") {
            alert(`${data.err}`);
        }
        if (key[0] == "formerr") {
            alert(`${data.formerr}`);
        }
        if (key[0] == "method") {
            alert(`${data.method}`);
        }
    } catch (error) {
        alert("Server error");
    }
    form.reset();
});