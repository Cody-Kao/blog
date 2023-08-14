/* 使用localStorage 把使用者按讚的留言都render liked class
window.onload = async function(){
    var csrfToken = document.querySelector("input[name='csrf_token']").value; 印出csrf token
    console.log(csrfToken)
    for (var i = 0; i < localStorage.length; i++){
        if (localStorage.getItem(localStorage.key(i)) === "true"){
            document.querySelector(`#${localStorage.key(i)}`).querySelector(".button.dark").classList.add('liked');
        }
    }
}
*/

function show_more_content(btn){
    let comment = btn.parentElement;
    comment.querySelector(".dots").classList.toggle("hide"); // 能toggle class，如果有該class就移除，如果沒有就新增
    comment.querySelector(".more").classList.toggle("hide");
    btn.textContent == "Read More" ? btn.textContent = "Read Less" : btn.textContent = "Read More";
}

function show_more_comments(btn){
    let rest_comments = btn.parentElement.querySelector('.more-comments-area');
    let show_less_comments_btn = btn.parentElement.querySelector('.show-less-comments');
    rest_comments.classList.toggle('hide');
    btn.classList.toggle('hide');
    show_less_comments_btn.classList.toggle('hide');
}

function show_less_comments(btn){
    let rest_comments = btn.parentElement.querySelector('.more-comments-area');
    let show_more_comments_btn = btn.parentElement.querySelector('.show-more-comments');
    rest_comments.classList.toggle('hide');
    btn.classList.toggle('hide');
    show_more_comments_btn.classList.toggle('hide');
}

async function thumb_toggle(btn, authenticated){
    if (authenticated != 'False'){
        var csrfToken = document.querySelector("input[name='csrf_token']").value;
        let commentId = btn.closest('div.comment').id.slice(8);
        let likes = btn.closest('.comment').querySelector('.likes');
        if (btn.classList.contains('liked')){
            likes.innerText = parseInt(likes.innerText) + 1; // 要轉成int去加 不然會變成string的concat
            var like = 1;
        }else{
            var like = -1;
            likes.innerText = parseInt(likes.innerText) - 1;
        }

        fetch(`${window.location.origin}/comment/${commentId}/thumb_toggle`, { // js string interpolation ==> `${variable}` like f-string in python
            method:'POST',
            headers:{
                'X-CSRF-TOKEN':csrfToken,
                'Content-type':'application/json' // 送json格式必加
            },
            body:JSON.stringify({ // 送json格式必加
                change:like
            })
            
        })
        .then(res=>{ // 這個是promise based的 response，由fetch return而來
            if (res.ok){ // 因為單純的catch不會抓這種404等等的錯誤，所以要加這行去判斷status code
                console.log('HTTP request successful');
            } else{
                console.log('HTTP request not successful');
            }
            return res; // 把response傳下去
        })
        .then(res=> res.json()) // 拿到response之後轉成json格式再傳下去 arrow function 會讓後面這行自動處理成return的格式
        .then(data=> console.log(data))
        .catch(error=> console.log('Error')) // 抓取其他的錯誤(syntax error or no internet connection)
    }else{
        return;
    }
};

function clicking(button, authenticated){
    console.log(authenticated);
    if (authenticated != 'False'){
        button.classList.toggle('liked');
        if(button.classList.contains('liked')) {
            gsap.fromTo(button, {
                '--hand-rotate': 8
            }, {
                ease: 'none',
                keyframes: [{
                    '--hand-rotate': -45,
                    duration: .16,
                    ease: 'none'
                }, {
                    '--hand-rotate': 15,
                    duration: .12,
                    ease: 'none'
                }, {
                    '--hand-rotate': 0,
                    duration: .2,
                    ease: 'none',
                    clearProps: true
                }]
            })
        }
    }else{
        alert('請先登入')
        return
    }
}

function toggle_reply_form(btn){
    let form = btn.parentElement.parentElement.parentElement.querySelector('.reply-form')
    form.classList.toggle('d-none')
}

function close_reply_form(btn){
    let form = btn.parentElement.parentElement
    form.classList.add('d-none')
}

async function createReply(btn, postId, commentId){
    let textarea = btn.parentElement.parentElement.querySelector('textarea');
    let textContent = textarea.value;
    //console.log(textarea.value); debug用的
    if (textContent == ''){
        alert('留言不得為空');
        return;
    }
    var csrfToken = document.querySelector("input[name='csrf_token']").value; // 取得csrf token
    let replySection = btn.closest('div.comment-content').nextElementSibling; // closest是找父節點用的 同層或底層不行
    textarea.value = '';
    let stripedTagTextContent = textContent.replace(/(<([^>]+)>)/gi, "") // 用前端來把html tag remove掉
    fetch(`${window.location.origin}/reply/${postId}/${commentId}`, { // js string interpolation ==> `${variable}` like f-string in python
        method:'POST',
        headers:{
            'X-CSRF-TOKEN':csrfToken, // 因為我們有設定csrf token所以要加在標頭一起送出驗證
            'Content-type':'application/json' // 送json格式必加
        },
        body:JSON.stringify({ // 送json格式必加
            content:stripedTagTextContent
        })
        
    })
    .then(res=>{ // 這個是promise based的 response，由fetch return而來
        if (res.ok){ // 因為單純的catch不會抓這種404等等的錯誤，所以要加這行去判斷status code
            console.log('HTTP request successful');
        } else{
            console.log('HTTP request not successful');
        }
        return res; // 把response傳下去
    })
    .then(res=>res.json())
    .then(res=> {replySection.innerHTML+=res.data;
                console.log(res.data)})
    .catch(error=> alert('請確認已登入，或請重整後再試 若仍有問題請來信告知問題 感謝!')) // 抓取其他的錯誤(syntax error or no internet connection)
};

function toggleUpdateDeleteCommentBtn(span){
    toggleDiv = span.parentElement.querySelector('.update-delete-comment-btn');
    toggleDiv.classList.toggle('expand');
}

function OnInput() {
    this.style.height = (this.scrollHeight) + 2 + "px";
  }

function editComment(btn, content, postId, commentId){
    let cancelBtn = btn.parentElement.querySelector('button.delete-btn')
    cancelBtn.innerText = "Cancel" 
    cancelBtn.setAttribute('data-bs-target', `#cancel-comment-${ commentId }-modal`)
    let contentDiv = btn.closest('div.comment-content').querySelector('div.content-div') // 先往上選父節點再往下找
    let submitInput = document.createElement('input')
    submitInput.setAttribute('type', 'submit')
    submitInput.setAttribute('form', `form-${commentId}`)
    submitInput.setAttribute('value', 'submit')
    btn.parentElement.replaceChild(submitInput, btn) //替換原本的edit button成submit input
    let formArea = document.createElement('form')
    formArea.setAttribute('id', `form-${commentId}`)
    formArea.setAttribute('method', 'POST')
    formArea.setAttribute('action', `/edit/comment/${postId}/${commentId}`)
    let textArea = document.createElement('textarea')
    textArea.setAttribute('name', 'new_content')
    textArea.style.height = "50px"
    textArea.classList.add('form-control')
    textArea.addEventListener("input", function() {
        textArea.style.height = (this.scrollHeight) + 2 + "px";
    });
    let hiddenInput = document.createElement('input')
    hiddenInput.setAttribute('type', 'hidden')
    hiddenInput.setAttribute('name', 'csrf_token')
    hiddenInput.setAttribute('value', document.querySelector("input[name='csrf_token']").value)
    formArea.appendChild(hiddenInput)
    formArea.appendChild(textArea)
    contentDiv.innerHTML = '' // 先清空innerHTML 讓我們append之後不會殘留原本的資料
    contentDiv.appendChild(formArea) // 如果是創造一個DOM object就只能用appendChild的方式放入innerHTML 除非是string才能直接assign
    setTextAreaValueAndExpand(textArea, content);
    
}

// Function to set textarea value and trigger auto-expand
function setTextAreaValueAndExpand(textarea, content) {
    textarea.value = content;

// Manually trigger the 'input' event after setting the value
    const event = new Event("input", {
        bubbles: true,
        cancelable: true,
    });
    textarea.dispatchEvent(event);
}

