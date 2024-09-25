const datas = document.getElementById("datas").innerHTML;
const product = JSON.parse(datas);
const productId = product.id;
const payedNumbers = [10, 5, 32, 22];
const reseivedNumbers = [4, 16, 20, 40];
const btnAddToCart = document.getElementById("pay");
const numbers = document.getElementById("numbers");
const totalValue = document.getElementById("totalValue");
const size = String(product.numberQuantity).length;
const productNumbers = new Object();
const selectedNumbers = new Array();
const styleDisponible = "col btn btn-outline-secondary";
const styleReseived = "col btn btn-warning";
const stylePayed = "col btn btn-success";
const styleReseivedCurrent = "col btn btn-outline-warning";
const reseivedCurrentList = new Array();
let cart = Cookies.get("cart") ? JSON.parse(Cookies.get("cart")) : {cart: {}};

if(cart.cart[productId]) {
  reseivedCurrentList.push(...cart.cart[productId]);
} else {
  cart.cart[productId] = [];
}

function getSelectedNumbers() {
  if(reseivedCurrentList.length > 0) {
    selectedNumbers.concat(reseivedCurrentList)
  }
  return selectedNumbers;
}

function addToCart(productId, numbers) {
  if(!cart.cart[productId]) {
    cart.cart[productId] = [];
  }
  cart.cart[productId].push(...numbers);
}

function addUserOrder() {
  fetch(`/cart/${productId}/`, {
    method: "POST",
    headers: {
      "Context-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(cart)
  })
  .then(response => {
    return response.json()
  })
  .catch(error => {
    console.error(error)
  })
}

btnAddToCart.addEventListener("click", () => {
  const selectedNumbers = getSelectedNumbers();

  if(selectedNumbers.length < product.minQuantity) {
    window.alert("Selecione os números", `Quantidade mínima ${product.minQuantity}`)
  }

  if(user === "AnonymousUser") {
    addToCart(productId, selectedNumbers);
    Cookies.set("cart", JSON.stringify(cart), { path: "/" });
  }

  addUserOrder();
});

document.addEventListener("DOMContentLoaded", async (event) => {
  for(let number = 1; number < product.numberQuantity; number++) {
    let li = document.createElement("li");
    let paddedNumber = number.toString().padStart(size, "0");
    li.innerText = paddedNumber;
    li.setAttribute("id", number);

    if(payedNumbers.includes(number)) {
      li.setAttribute("class", stylePayed)
    } else if(reseivedNumbers.includes(number)) {
      li.setAttribute("class", styleReseived)
    } else if(reseivedCurrentList.includes(number)) {
      li.setAttribute("class", styleReseivedCurrent);
      li.setAttribute("onClick", `updateNumber(${number})`);
    } else {
      li.setAttribute("class", styleDisponible)
      li.setAttribute("onClick", `updateNumber(${number})`)
    }

    numbers.appendChild(li);
  }
})

function updateNumber(number) {
  let elementId = document.getElementById(String(number))
  
  if(selectedNumbers.includes(number)) {
    let index = selectedNumbers.indexOf(number);
    selectedNumbers.splice(index, 1);
    elementId.setAttribute("class", styleDisponible);
  } else if(reseivedCurrentList.includes(number)) {
    reseivedCurrentList.split(reseivedCurrentList.indexOf(number));
    li.setAttribute("class", styleReseivedCurrent);
    li.setAttribute("onClick", `updateNumber(${number})`);
  } else {
    selectedNumbers.push(number);
    elementId.setAttribute("class", styleReseivedCurrent);
  }
  
  result = product.price * selectedNumbers.length;
  totalValue.innerText = result.toString().replace(".", ",");
}