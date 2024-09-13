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
  const response = await fetch(`/wishlist/${styleid}`);
  try {

  const data = await response.json();
  console.log(data);
    
  } catch (error) {
    alert(error);
  }
}
