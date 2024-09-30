const form = document.getElementById("styleForm");

form.addEventListener("submit", async (event) => {
    event.preventDefault(); //preventDefault submission

    const formData = new FormData(form)

    try {
        const response = await fetch("/createStyle", {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        if (response.status != 200) {
            alert(data.error);
        }
        if (response.status === 200) {
            alert(data.message);
        }

    } catch (error) {
        alert("Server error")
    }

})