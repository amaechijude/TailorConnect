// const form = document.getElementById("reviewForm");

// form.addEventListener("submit", async (event) => {
//   event.preventDefault(); //prevent default form submission

//   const formData = new FormData(form);
//   const styleId = document.getElementById("styleId").value;
// //   formData.append("CustomField", "This is some extra data");

//   const response = await fetch(`/review/${styleId}`, {
//     method: "POST",
//     body: formData,
//   });

//   const data = await response.json();
//   //process the response
//   console.log(data);
// });

async function WishList(styleid) {

    const response = await fetch(`/add_wishlist/${styleid}`);
    const data = await response.json();
    console.log(data);

    const keys = Object.keys(data);
    if (keys[1] == "wcount") {
        const count = data.wcount;
        const wishcount = document.getElementById("wishcount");
        wishcount.textContent = count;  
    }
    if (keys[0] == "add") {
        const button = document.getElementById(`btn_${styleid}`);
        button.textContent = "Added to wishlist ";
        button.className = "btn btn-danger w-100";
        alert(data.add);
    }
    if (keys[0] == "err") {
        alert(data.err);
    }

}

async function RmWishList(styleid) {

    const response = await fetch(`/rm_wishlist/${styleid}`);
    const data = await response.json();
    console.log(data);

    const div = document.getElementById(`${styleid}`);
    div.remove();

}