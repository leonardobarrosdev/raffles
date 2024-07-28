const tbodyFragment = document.querySelector("tbody")
const itemsQuantity = Number(tbodyFragment.dataset.itemsquantity)

function cartByCookies() {
  // create elements for tbody
  const data = fetch(`/subitems/`, {
    method: "GET",
  })
  .then(response => {
    return response.json()
  })
  .catch(error => {
    console.error("Probablity haven't sub items on cart; ", error)
  })

  for(let field of data) {
    let tr = document.createElement("tr")
    let tdTitle = createElement("td")
    let tdNumbers = document.createElement("td")
    let tdPrice = document.createElement("td")
    let tdQuantity = document.createElement("td")

    tdTitle.innerText = field.title
    tdNumber.innerText = "#"
    tdPrice.innerText = field.price
    tdQuantity.innerText = field.get_total_price

    tr.appendChild(tdTitle)
    tr.appendChild(tdNumbers)
    tr.appendChild(tdPrice)
    tr.appendChild(tdQuantity)

    bodyFragment.appendChild(tr)
  }
}

if(itemsQuantity > 0) {
  cartByCookies()
}
