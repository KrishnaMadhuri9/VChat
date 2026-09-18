function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

function likefunction(feedId){   
    let likeelement=document.getElementById('likeIcon'+feedId);
    
    let isLiked=likeelement.classList.contains('fa-solid')
    
    fetch(`/like/${feedId}/`,{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken":getCookie("csrftoken")
        },
        body:JSON.stringify({
            "liked": !isLiked
        })
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if(data.liked){
            likeelement.classList.remove('fa-regular');
            likeelement.classList.add('fa-solid');
        }
        else{
            likeelement.classList.add('fa-regular');
            likeelement.classList.remove('fa-solid');
        }

        if(data.likecount !== 0){
            document.getElementById("likecount"+feedId).innerText=data.likecount;
        }
        else{
            document.getElementById("likecount"+feedId).innerText="Like";
        }
    })
    .catch(error=>console.log(error));
}

let currentFeedId=null;

function openCommentModal(feedId){
    currentFeedId=feedId;
    document.getElementById("commentModal").style.display="flex";
    loadComments(feedId);
}

function closeCommentModal(){
    document.getElementById("commentModal").style.display="none";
    document.getElementById("commentText").value="";
}

function loadComments(feedId){
    fetch(`/comments/${feedId}/`)
    .then(response =>response.json())
    .then(data => {
        let html="";
        data.comments.forEach(comment => {
            html+=
            `<div class="comment-item">
                <b>${comment.user}</b>
                <p>${comment.comment}</p>
                ${comment.is_owner ? 
                `<button class="delete-btn" onclick="deleteComment(${comment.id})"> Delete</button>`:""}
            </div>`
            ;
        });
        document.getElementById("commentList").innerHTML=html;
    })
    .catch(error => console.log(error));
}

function postComment(){
    let comment=document.getElementById("commentText").value;
    fetch(`/comment/${currentFeedId}/`,{
            method:"POST",
            headers:{
                "Content-Type":"application/json",
                "X-CSRFToken":getCookie("csrftoken")
            },
            body:JSON.stringify({
                comment:comment
            })

    })
    .then(response=>response.json())
    .then(data=>{
        document.getElementById("commentText").value="";
        loadComments(currentFeedId);
        document.getElementById("commentcount"+currentFeedId).innerText=data.commentcount;
    });
}

function deleteComment(commentId){

    if(!confirm("Delete comment?"))
        return;

    fetch(`/delete-comment/${commentId}/`,{
            method:"POST",
            headers:{
                "X-CSRFToken":getCookie("csrftoken")
            }
    })
    .then(response=>response.json())
    .then(data=>{
        loadComments(currentFeedId);
        document.getElementById("commentcount"+currentFeedId).innerText=data.commentcount;
    });
}

function shareFeed(feedId){
    fetch(`/share/${feedId}/`,{
        method:"POST",
        headers:{
            "X-CSRFToken":getCookie("csrftoken")
        }
    })
    .then(response=>response.json())
    .then(data=>{
        document.getElementById("sharecount"+feedId).innerText=data.sharecount;
        alert(data.message);
        // Reload timeline to show the shared post
        location.reload();
    });
}


function toggleMenu() {
    const dropdown = document.getElementById("hamburgerDropdown");

    if (dropdown) {
        dropdown.classList.toggle("show");
    }
}