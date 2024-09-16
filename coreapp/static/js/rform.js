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
        console.log(data);
        const key = Object.keys(data);

        if (key[0] == "rev") {
            // create new div and add the response to it

            alert("review added");
        }
        if (key[0] == "err") {
            alert("you need to log in");
        }
        if (key[0] == "bad") {
            alert("bad request");
        }
    } catch (error) {
        alert("Server error");
    }
    form.reset();
});