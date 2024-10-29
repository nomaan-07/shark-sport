const getAndShowAllProducts = async (pageNumber, limit) => {
  const productListWrapperElem = document.getElementById("product-list");
  const skip = (pageNumber - 1) * limit;
  const response = await fetch(
    `http://localhost:8000/api/product/products/?skip=${skip}&limit=${limit}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  const products = await response.json();
  //   productListWrapperElem.innerHTML = "";
  products.forEach((product) => {
    productListWrapperElem.insertAdjacentHTML("beforeend", ``);
    console.log(product);
  });
  console.log(products);
};

export { getAndShowAllProducts };
