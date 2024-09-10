function sendArticleComment(articleID) {
    //console.log('submit send comment');
    var comment = $('#CommentText').val(); // value of textarea with id CommentText
    var parent_id = $('#parent_id').val();

    // send get request to address in background and wait for resposnse (res)
    // we can send a json format (like dictionary) along to request with specific key-value

    $.get('/articles/add-article-comment/', {
        article_comment: comment, article_id: articleID, parent_id: parent_id,
    }).then(res => {
        $('#comments_area').html(res);
        $('#CommentText').val('');
        $('#parent_id').val('');
        if (parent_id !== null && parent_id !== '') {
            document.getElementById('single-comment-box-' + parent_id).scrollIntoView({behavior: "smooth"});
        } else {
            document.getElementById('comments_area').scrollIntoView({behavior: "smooth"});
        }
    });
}

function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('start_form').scrollIntoView({behavior: "smooth"});
}

function filterPrice() {
    const filterPrice = $('#sl2').val();
    const start_price = filterPrice.split(',')[0];
    const end_price = filterPrice.split(',')[1];
    $('#start_price').val(start_price);
    $('#end_price').val(end_price);
    $('#filter_price_form').submit();
}


function fillPage(page) {
    $('#page').val(page);
    $('#filter_price_form').submit();
}


function showLargeImage(imagesrc) {
    $('#large_image').attr('src', imagesrc);
    $('#show_large_image_modal').attr('href', imagesrc);

}


function addProductToOrder(productId) {
    const requestedCount = $('#counter').val();
    $.get('/order/add-to-order?product_id=' + productId + '&requested_count=' + requestedCount).then(res => {
        console.log(res);
        Swal.fire({
            title: "اعلان",
            text: res.text,
            icon: res.icon,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            showCancelButton: res.cancel_button_show,
            confirmButtonText: res.confirm_button_text,
            cancelButtonText: res.cancel_button_text,

        }).then((result) => {
            if(result.isConfirmed && res.status=='not logged in'){
                window.location.href='/login';
            }
        });
    });
}


function removeOrderDetail(selectedProductId){
    $.get('/user-panel/remove-order-detail?selected_product_id=' + selectedProductId).then(res => {
    if(res.status=='success'){
        $('#order-detail-content').html(res.data);
    }
    });
}

function changeOrderDetailCount(selectedProductId, state){
    $.get('/user-panel/change-order-detail?selected_product_id=' + selectedProductId + '&state=' + state).then(res => {
    if(res.status=='success'){
        $('#order-detail-content').html(res.data);
    }
    });
}

