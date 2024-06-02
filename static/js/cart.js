const updateBtn = document.getElementByClassName("update_cart");

for(i = 0; 1 < updateBtn.length; i++){
  updateBtn[i].addEventListener("click", () => {
    const productId = this.dataset.product;
    const action = this.dataset.action;
    if(user == "AnonymousUser"){
      console.log("User is not authenticated");
    } else {
      updateUserOrder(productId, action);
    }
  });
};

function updateUserOrder(productId, action){
  const url = "/update_item"
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({"productId": productId, "action": action})
  }).then(response) => {
    return response.json();
  }.then((data) => {
    console.log("Data", data);
    location.reload()
  })
}
