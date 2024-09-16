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

async function RmWishList(styleid) {

    const response = await fetch(`/rm_wishlist/${styleid}`);
    const data = await response.json();
    console.log(data);
    const keys = Object.keys(data);
    if (keys[1] == "wcount") {
        const count = data.wcount;
        const wishcount = document.getElementById("wishcount");
        wishcount.textContent = count;
    }
    const div = document.getElementById(`${styleid}`);
    div.remove();

}

// If styles exist
async function iaddWishList(styleid) {
    try {
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
            const rm_btn = document.getElementById(`btn_${styleid}_irm`);
            const add_btn = document.getElementById(`btn_${styleid}_iadd`);

            add_btn.style.display = 'none';
            rm_btn.style.display = 'block';
        }
    } catch (error) {

    }
}

async function irmWishlist(styleid) {
    try {
        const response = await fetch(`/rm_wishlist/${styleid}`);
        const data = await response.json();
        console.log(data);
        const key = Object.keys(data);
        if (key[1] == "wcount") {
            const count = data.wcount;
            const wishcount = document.getElementById("wishcount");
            wishcount.textContent = count;
        }
        if (key[0] == "removed") {
            const rm_btn = document.getElementById(`btn_${styleid}_irm`);
            const add_btn = document.getElementById(`btn_${styleid}_iadd`);

            rm_btn.style.display = 'none';
            add_btn.style.display = 'block';
        }
        if (key[0] == "err") {
            alert(data.err);
        }
    } catch (error) {

    }
}

// If not styles
async function naddWishlist(styleid) {
    try {
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
            const rm_btn = document.getElementById(`btn_${styleid}_nrm`);
            const add_btn = document.getElementById(`btn_${styleid}_nadd`);

            add_btn.style.display = 'none';
            rm_btn.style.display = 'block';
        }
    } catch (error) {

    }
}

async function nrmWishlist(styleid) {
    try {
        const response = await fetch(`/rm_wishlist/${styleid}`);
        const data = await response.json();
        console.log(data);
        const key = Object.keys(data);
        if (key[1] == "wcount") {
            const count = data.wcount;
            const wishcount = document.getElementById("wishcount");
            wishcount.textContent = count;
        }
        if (key[0] == "removed") {
            const rm_btn = document.getElementById(`btn_${styleid}_nrm`);
            const add_btn = document.getElementById(`btn_${styleid}_nadd`);

            rm_btn.style.display = 'none';
            add_btn.style.display = 'block';
        }
        if (key[0] == "err") {
            alert(data.err);
        }
    } catch (error) {

    }
}