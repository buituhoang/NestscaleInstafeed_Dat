let cart_footer = document.getElementsByClassName('cart__footer')[0]
let quantity = document.getElementById('shopify-section-template--18269752590620__main')
if(cart_footer){
    cart_footer.innerHTML += 'Duoc giam gia ne'
}

if(quantity){
    let content = '<div id="app-shopify-id"/>'
    quantity.outerHTML += content
}

let script = document.createElement('script');
        script.type = 'text/javascript';
        script.id = 'nestscale-nestdesk-script'
        script.src = 'https://odoo.website/bought_together/static/js/shopify.js';
        document.head.appendChild(script);