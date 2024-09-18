const form = document.getElementById("styleForm");

form.addEventListener("submit", async (event) => {
    event.preventDefault(); //preventDefault submission
    
    const formData = new FormData(form)
    
    const response = await fetch("/createStyle", {
        method: 'POST',
        body: formData,
    });
    const data = await response.json();
    console.log(data);
    // process response logic
    
})