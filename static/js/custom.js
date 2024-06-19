function articleCommentText(articleId){
    var comment = $('#commentText').val();
    var parentId = $('#parent_id').val();
    $.get('/articles/add_article_comment',{
        article_comment: comment,
        article_id : articleId,
        parent_id : parentId
    }).then(res => {
        console.log(res);
        $('#comment_area').html(res);
        $('#commentText').val('');
        $('#parentId').val('');
        if(parentId !== null){
            document.getElementById("single_comment_box "+ parentId).scrollIntoView({behavior:'smooth'})
        }
        else {
            document.getElementById("comment_area").scrollIntoView({behavior:'smooth'})
        }
    })
}

function fillParentId(parentId){
    $('#parent_id').val(parentId)
    document.getElementById('comment_form').scrollIntoView({behavior:"smooth"})
}

function filterProducts(){
    debugger;
    const filterPrice= $('#sl2').val();
    const start_price= filterPrice.split(',')[0];
    const end_price= filterPrice.split(',')[1];
    $('#start_price').val(start_price);
    $('#end_price').val(end_price);
    $('#filter_form').submit();
}

function addProductToOrder(ProductId){
    console.log(ProductId);
    const productCount= $('#product_count').val();
    $.get('/orders/add_to_order?product_id=' + ProductId + '&count=' + productCount).then(res => {
            Swal.fire({
                title: "اعلان",
                text: res.text,
                icon: res.icon,
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                confirmButtonText: res.confirmButtonText
            });
    });
}

function removeOrderDetail(detailId){
    $.get('/user/remove-order-basket?detail_id=' + detailId).then(res => {
        if (res.status === 'success'){
            $('#order_detail_content').html(res.body);
        }
    });
}


function changeOrderDetailCount(detailId , state){
     $.get('/user/change-order-basket?detail_id=' + detailId + '&state=' + state).then(res => {
        if (res.status === 'success'){
            $('#order_detail_content').html(res.body);
        }
    });
}