const form = document.getElementById("styleForm");

form.addEventListener("submit", async (event) => {
    event.preventDefault(); //preventDefault submission

    const formData = new FormData(form)

    try {
        const response = await fetch("/createStyle", {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) {
            const data = await response.json();
            alert(data.error);
        }
        if (response.ok) {
            const data = await response.json();
            alert(data.message)
        }

    } catch (error) {
        alert("Server error")
    }

})