function like_post(element) {
    let id = element.dataset.post_id;
    console.log("like_post")
    fetch('/post/' + parseInt(id) + '/like', {
        method: 'PUT'
    })
        .then(response => {
            if (response.ok) {
                let count = element.querySelector('.likes_count');
                let value = parseInt(count.innerHTML);
                value++;
                count.innerHTML = value;
                element.querySelector('.svg-span').innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
                </svg>`;
                element.setAttribute('onclick', 'unlike_post(this)');
            } else {
                console.log('Failed to like post.');
            }
        })
        .catch(error => {
            console.log('Error occurred while liking post:', error);
        });
}

function unlike_post(element) {
    let id = element.dataset.post_id;
    console.log("un_like_post")
    fetch('/post/' + parseInt(id) + '/unlike', {
        method: 'PUT'
    })
        .then(response => {
            if (response.ok) {
                let count = element.querySelector('.likes_count');
                let value = parseInt(count.innerHTML);
                value--;
                count.innerHTML = value;
                element.querySelector('.svg-span').innerHTML = `
                <svg width="1.1em" height="1.1em" viewBox="0 -1 16 16" class="bi bi-heart" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M8 2.748l-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
                </svg>`;
                element.setAttribute('onclick', 'like_post(this)');
            } else {
                console.log('Failed to unlike post.');
            }
        })
        .catch(error => {
            console.log('Error occurred while unliking post:', error);
        });
}

function save_post(element) {
    let id = element.dataset.post_id;
    fetch('/post/' + parseInt(id) + '/save', {
        method: 'PUT'
    })
        .then(response => {
            if (response.ok) {
                let count = element.querySelector('.savers_count');
                let value = count.innerHTML;
                value++;
                count.innerHTML = value;
                element.querySelector('.svg-span').innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" 
                                                                height="16" fill="currentColor"
                                     class="bi bi-bookmarks-fill" viewBox="0 0 16 16">
                                    <path d="M2 4a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v11.5a.5.5 0 0 1-.777.416L7 13.101l-4.223 2.815A.5.5 0 0 1 2 15.5V4z"/>
                                    <path d="M4.268 1A2 2 0 0 1 6 0h6a2 2 0 0 1 2 2v11.5a.5.5 0 0 1-.777.416L13 13.768V2a1 1 0 0 0-1-1H4.268z"/>
                                    </svg>`;
                element.setAttribute('onclick', 'unsave_post(this)');
            } else {
                console.log('Failed to save post.');
            }
        })
        .catch(error => {
            console.log('Error occurred while saving post:', error);
        });
}

function unsave_post(element) {
    let id = element.dataset.post_id;
    fetch('/post/' + parseInt(id) + '/unsave', {
        method: 'PUT'
    })
        .then(response => {
            if (response.ok) {
                let count = element.querySelector('.savers_count');
                let value = count.innerHTML;
                value--;
                count.innerHTML = value;
                element.querySelector('.svg-span').innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                             fill="currentColor" class="bi bi-bookmarks" viewBox="0 0 16 16">
                                            <path d="M2 4a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v11.5a.5.5 0 0 1-.777.416L7 13.101l-4.223 2.815A.5.5 0 0 1 2 15.5V4zm2-1a1 1 0 0 0-1 1v10.566l3.723-2.482a.5.5 0 0 1 .554 0L11 14.566V4a1 1 0 0 0-1-1H4z"/>
                                            <path d="M4.268 1H12a1 1 0 0 1 1 1v11.768l.223.148A.5.5 0 0 0 14 13.5V2a2 2 0 0 0-2-2H6a2 2 0 0 0-1.732 1z"/>
                                        </svg>`;
                element.setAttribute('onclick', 'save_post(this)');
            } else {
                console.log('Failed to unsave post.');
            }
        })
        .catch(error => {
            console.log('Error occurred while unsaving post:', error);
        });
}

function get_comments(post_id) {
    fetch('/comments/' + parseInt(post_id), {
        method: 'GET',
    })
        .then(response => {
            if (response.ok) {
                console.log(response.status)
                return response.json();
            } else {
                throw new Error('Failed to fetch comments.');
            }
        })
        .then(comments => {
            const commentsDiv = document.getElementById('comments-div');
            commentsDiv.setAttribute('data-id_post', post_id);
            commentsDiv.innerHTML = '';

            comments.forEach(comment => {
                const commentElement = createCommentElement(comment);
                commentsDiv.appendChild(commentElement);
            });
        })
        .catch(error => {
            console.log('Error occurred while fetching comments:', error);
        });
}

function addComment() {
    const element = document.getElementById('comments-div');
    const post_id = element.getAttribute('data-id_post');
    const commentTextarea = document.getElementById('comment-text');
    const commentText = commentTextarea.value;
    const data = {
        'commentText': commentText,
        'post_id': post_id
    };

    fetch('/add_comment/', {
        method: 'PUT',
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                console.log(response.status)
                return response.json();
            } else {
                throw new Error('Failed to add comment.');
            }
        })
        .then(comment => {
            const commentsDiv = document.getElementById('comments-div');
            const commentElement = createCommentElement(comment);
            commentsDiv.insertBefore(commentElement, commentsDiv.firstChild);
            commentTextarea.value = '';
            let cmtCountElement = document.querySelector(`div.post[data-post_id="${post_id}"] .cmt-count`);
            let currentValue = parseInt(cmtCountElement.innerHTML);
            let updatedValue = currentValue + 1;
            cmtCountElement.innerHTML = updatedValue.toString();
        })
        .catch(error => {
            console.log('Error occurred while adding comment:', error);
        });
}

function deleteComment(element) {
    let id = element.getAttribute('data-comment_id');
    let post_id = element.parentElement.getAttribute('data-id_post');
    let data = {
        'comment_id': id
    };

    fetch('/delete_comment/', {
        method: 'PUT',
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                console.log(response.status)
                cmtCountElement = document.querySelector(`div.post[data-post_id="${post_id}"] .cmt-count`);
                let currentValue = parseInt(cmtCountElement.innerHTML);
                let updatedValue = currentValue - 1;
                cmtCountElement.innerHTML = updatedValue.toString();
                element.remove();
            } else {
                throw new Error('Failed to delete comment.');
            }
        })
        .catch(error => {
            console.log('Error occurred while deleting comment:', error);
        });
}

function get_messages(chat_id) {
    const messagesScrollbar = document.getElementById('messages-scrollbar');
    const messagesDiv = document.getElementById('messages-div');
    messagesDiv.setAttribute('data-chat_id', chat_id);
    fetch('/messages/' + parseInt(chat_id), {
        method: 'GET',
    })
        .then(response => {
            if (response.ok) {
                console.log(response.status);
                return response.json();
            } else {
                throw new Error('Failed to fetch messages.');
            }
        })
        .then(messages => {
            messagesDiv.innerHTML = '';
            messages.forEach(message => {
                const messageElement = createMessageElement(message);
                messagesDiv.appendChild(messageElement);
            });
            messagesScrollbar.scrollTop = messagesScrollbar.scrollHeight;
        })
        .catch(error => {
            console.log('Error occurred while fetching messages:', error);
        });

}

function sendMessage() {
    const element = document.getElementById('messages-div');
    let chat_id = element.getAttribute('data-chat_id');
    const messageTextarea = document.getElementById('message-text');
    const messagesScrollbar = document.getElementById('messages-scrollbar')
    const messageText = messageTextarea.value;
    if (chat_id == null) {
        chat_id = current_chat_id;
        console.log(current_chat_id)
    }
    const data = {
        'messageText': messageText,
        'chat_id': chat_id
    };
    console.log(JSON.stringify(data))
    fetch('/add_message/', {
        method: 'PUT',
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                console.log(response.status)
                return response.json();
            } else {
                throw new Error('Failed sending message...');
            }
        })
        .then(message => {
            const messagesDiv = document.getElementById('messages-div');
            const messageElement = createMessageElement(message);
            messagesDiv.appendChild(messageElement)
            messageTextarea.value = '';
            messagesScrollbar.scrollTop = messagesScrollbar.scrollHeight;
        })
        .catch(error => {
            console.log('Error occurred while adding comment:', error);
        });

}

function createMessageElement(message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message-text-div';
    messageElement.setAttribute('data-message_id', message.id);
    const isCurrentUser = (message.sender.username === current_username_auth);
    if (isCurrentUser) {
        messageElement.classList.add('message-text-div-right');
    } else {
        messageElement.classList.add('message-text-div-left');
    }
    messageElement.innerHTML = `
        <strong id="username-comment" style="font-size: 12px; text-decoration: underline;">@${message.sender.username}</strong>
        <br>
        ${message.content}`;
    return messageElement;
}

function generateDeleteButton(comment_username) {
    if (current_username_auth === comment_username) {
        return `
      <button type="button" class="close" id="delete-comment-button" onclick="deleteComment(this.parentNode)" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>`;
    }
    return '';
}

function createCommentElement(comment) {
    const commentElement = document.createElement('div');
    commentElement.className = 'comment-text-div';
    commentElement.setAttribute('data-comment_id', comment.id);
    commentElement.innerHTML = `
        <div class="small-profilepic" style="width: 20px; height: 20px; border-radius: 50%; background-image: url(${comment.commenter.profile_pic});"></div>
        <a href="/profile/${comment.commenter.username}">
            <strong id="username-comment" style="color: black; font-size: 12px; text-decoration: underline;">@${comment.commenter.username}</strong>
        </a> <br>${comment.body}
        ${generateDeleteButton(comment.commenter.username)}`;

    return commentElement;
}

function displaySelectedImage() {
    document.querySelector('#img-div').style.display = 'block';
    let preview = document.querySelector('#img-div');
    let input = document.getElementById('customFile');
    let file = input.files[0];
    let reader = new FileReader();
    reader.readAsDataURL(file)
    reader.onloadend = function () {
        preview.style.backgroundImage = `url(${reader.result})`;
    }
}

function adjustTextareaHeight(textareaId) {
    const textarea = document.getElementById(textareaId);
    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + "px";
}

function resetModalNewPost() {
    document.getElementById("post-text").value = "";
    document.getElementById("customFile").value = "";
    document.getElementById("img-div").innerHTML = "";
    document.getElementById("img-div").style.backgroundImage = "none";
    document.getElementById("img-div").style.display = "none";
    document.querySelector(".newpost").reset();
}

function resetCommentModal() {
    document.getElementById("comment-text").value = "";
    document.getElementById("comments-div").innerHTML = "";
}

function edit_post(element) {
    let postId = element.getAttribute("data-post_id");
    let editPostModel = document.getElementById("editPostModal");
    editPostModel.setAttribute("post-id", postId);
    document.getElementById("edit-post-text").value = document.querySelector("[data-post_id='" + postId + "'] .post-content").textContent.trim();
}

function delete_post() {
    const element = document.getElementById('editPostModal');
    let post_id = element.getAttribute("post-id");
    const data = {
        'post_id': post_id
    };
    fetch('/delete_post/', {
        method: 'PUT',
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                console.log(response.status)
                document.querySelector("[data-post_id='" + post_id + "'] ").remove()
                $('#editPostModal').modal('hide')
            } else {
                throw new Error('Failed removing post...');
            }
        })
        .catch(error => {
            console.log('Error occurred while removing post:', error);
        });
}

function edit() {
    const element = document.getElementById('editPostModal');
    let post_id = element.getAttribute("post-id");
    let contentText = document.getElementById("edit-post-text").value;
    const data = {
        'contentText': contentText,
        'post_id': post_id
    };
    fetch('/edit_post/', {
        method: 'PUT',
        body: JSON.stringify(data)
    })
        .then(response => {
            if (response.ok) {
                console.log(response.status)
                document.querySelector("[data-post_id='" + post_id + "'] .post-content").textContent = contentText;
                $('#editPostModal').modal('hide')
            } else {
                throw new Error('Failed editing post...');
            }
        })
        .catch(error => {
            console.log('Error occurred while editing post:', error);
        });
}

