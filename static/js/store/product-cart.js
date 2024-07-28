const pathname = window.location.pathname
const productId = pathname.split("/").at(-2)
const btnAddToCart = document.getElementById("pay")
const numbers = document.getElementById("numbers")
const totalValue = document.getElementById("totalValue")
const numberQuantity = Number(numberQuantityStr)
const size = numberQuantityStr.length
const productNumbers = new Object()
const selectedNumbers = new Array()
const styleDisponible = "col btn btn-outline-secondary"
const styleReseived = "col btn btn-warning"
const stylePayed = "col btn btn-success"
const styleReseivedCurrent = "col btn btn-outline-warning"
const objCart = JSON.parse(Cookies.get("cart")) || {"cart": []}
const reseivedCurrentList = objCart[productId]? objCart[productId] : []

document.addEventListener("DOMContentLoaded", async (event) => {
  for(let number = 1; number < numberQuantity; number++) {
    let li = document.createElement("li")
    let paddedNumber = number.toString().padStart(size, "0")
    li.innerText = paddedNumber
    li.setAttribute("id", number)

    if(payedNumbers.includes(number)) {
      li.setAttribute("class", stylePayed)
    } else if(reseivedNumbers.includes(number)) {
      li.setAttribute("class", styleReseived)
    } else if(reseivedCurrentList.includes(number)) {
      li.setAttribute("class", styleReseivedCurrent)
      li.setAttribute("onClick", `updateNumber(${number})`)
    } else {
      li.setAttribute("class", styleDisponible)
      li.setAttribute("onClick", `updateNumber(${number})`)
    }

    numbers.appendChild(li)
  }
})

function updateNumber(number) {
  let elementId = document.getElementById(String(number))
  
  if(selectedNumbers.includes(number)) {
    let index = selectedNumbers.indexOf(number)
    selectedNumbers.splice(index, 1)
    elementId.setAttribute("class", styleDisponible)
  } else if(reseivedCurrentList.includes(number)) {
    reseivedCurrentList.split(reseivedCurrentList.indexOf(number))
    li.setAttribute("class", styleReseivedCurrent)
    li.setAttribute("onClick", `updateNumber(${number})`)
  } else {
    selectedNumbers.push(number)
    elementId.setAttribute("class", styleReseivedCurrent)
  }
  
  result = price * selectedNumbers.length
  totalValue.innerText = result.toString().replace(".", ",")
}

function addUserOrder() {
  if(reseivedCurrentList) {
    selectedNumbers.concat(reseivedCurrentList)
  }

  objCart[productId] = selectedNumbers

  fetch(`/cart/${productId}/`, {
    method: "POST",
    headers: {
      "Context-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      "cart": objCart
    })
  })
  .then(response => {
    return response.json()
  })
  .catch(error => {
    console.error(error)
  })
}

btnAddToCart.addEventListener("click", () => {
  // if(selectedNumbers.length < minQuantity) {
  //   window.alert("Selecione os números", `Quantidade mínima ${minQuantity}`)
  // }
  
  if(objCart.productId) {
    delete objCart.productId
  }

  if(user == "AnonymousUser") {
    Cookies.remove("cart")

    if(reseivedCurrentList.length > 0) {
      selectedNumbers.concat(reseivedCurrentList)
    }
    
    objCart[productId] = selectedNumbers

    Cookies.set("cart", JSON.stringify(objCart))
  } else {
    addUserOrder()
  }
})
