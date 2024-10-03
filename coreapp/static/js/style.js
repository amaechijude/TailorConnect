
function StyleDiv(b_url, b_name, p_img, p_price, p_title, p_id, p_desc, p_url) {
    
    const superParentDiv = document.getElementById("spdiv");
    
    const shopNameDiv = document.createElement("div");
    shopNameDiv.classList = "shop-name-inside";
    shopNameDiv.style.textAlign = "center";
    const text = "Made By";
    shopNameDiv.appendChild(text);
    const break_tag = document.createElement("br");
    shopNameDiv.appendChild(break_tag);
    const sh_atag  = document.createElement("a");
    sh_atag.href = `${b_url}`;
    sh_atag.textContent = `${b_name}`
    shopNameDiv.appendChild(sh_atag);

    const productItemDiv = document.createElement("div");
    productItemDiv.className = "product-item";
    productItemDiv.appendChild(shopNameDiv);
    
    const hr_tag = document.createElement("hr");
    hr_tag.style.border = "1px solid #333";
    hr_tag.style.width = "100%";
    hr_tag.style.marginTop = "-0.5%";

    productItemDiv.appendChild(hr_tag);
    // product image
    const image = document.createElement("img")
    image.src = `${p_img}`;
    image.className = "product-image";
    productItemDiv.appendChild(image);
    // product page
    const h3_tag = document.createElement("h3");
    h3_tag.className = "product-title";
    h3_tag.textContent = `${p_title}`;
    const a_tag = document.createElement("a");
    a_tag.href = `${p_url}`;
    a_tag.appendChild(h3_tag);
    productItemDiv.appendChild(a_tag);
    //p _decription
    const p_tag = document.createElement("p");
    p_tag.className = "product-description";
    p_tag.textContent = `${p_desc}`;
    p_tag.style.textAlign = "center";
    productItemDiv.appendChild(p_tag);
    //price div
    const price_div = document.createElement("div");
    price_div.className = "product-price";
    price_div.textContent = `${p_price}`;
    productItemDiv.appendChild(price_div);
    //product page
    const btn_div = document.createElement("div");
    btn_div.style.display = "inline";
    const dt_btn = document.createElement("button");
    dt_btn.classList = "btn btn-outline-primary w-100";
    dt_btn.textContent = "Product Details";
    const a_tag1 = document.createElement("a");
    a_tag1.href = `${p_url}`;
    a_tag1.appendChild(dt_btn);
    btn_div.appendChild(a_tag1);
    btn_div.appendChild(break_tag);
    const dn_btn = document.createElement("button");
    dn_btn.classList = "btn btn-outline-danger w-100";
    dn_btn.textContent = "Archive";
    dn_btn.onclick = `archiveProduct(${p_id})`;
    btn_div.appendChild(dn_btn);

    productItemDiv.appendChild(btn_div);
    //finish
    const parentDiv = document.createElement("div");
    parentDiv.classList = "col-md-4 d-flex";
    parentDiv.appendChild(productItemDiv);

    superParentDiv.prepend(parentDiv);

}