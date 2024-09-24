index {
    home page to list styles **Done**
    Paginate the styles **Not yet Complete**
    Wishlist{
        Check if item in Wishlist **Done**
        if true or not {
            Remove wishlist Button {
                Set display of add to wishlist to none and swap on click"tRmWishlist(styleid)"

        }}
        **Done**

    }
    

}
profile {
    view and/or edit profile -- zindex with javascript **Done**
    view add and/or edit shipping address -- zindex with javascript **DONE**
    create designshop {
        recieveve details via form. **done**
        send emails to admins **done
    }
    view wishlist. **Done**
    view Orders
    view payments etc
}

every flexbox {
    **like** with async fetch api
}

product details {
    view ***Done***
    url ***Done***
    template **Done**

Next {
    edit brand details from shops page **Done**
    Edit style/products from shops **done**
    add reviews forms urls etc **done**
    
    Paginate styles{
        everywhere: index, wishlist, shop, etc
    }
}


**Buy button** {
    trigger
    form to add measurement and/or size in shipping address;
    ask for confirmation
    create order mark not paid:

    Use javascript to warn on trying to close tab closing

    grab the price and redirect to confirm html template {
        display the product and the price for confirmation
        send a post request to the backend {
            grab the Paystack secret key, user_email and amount
            parse it into the request made by the request library
            grab the access code from the response
            redirect to the frontend with the access code

            resume transaction from the frontend {
                const popup = new Paystack()
                popup.resumeTransaction(access_code)
                // handle response
            }
            
        }

    }
