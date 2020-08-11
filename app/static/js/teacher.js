function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    if(auth2.isSignedIn.get()){
        auth2.signOut();
        auth2.signOut().then(function () {
        console.log('User signed out.');
        Cookies.remove('userID');
        });
    }
    else{
        Cookies.remove('userID');
    }
}

window.onLoadCallback = function(){
    gapi.load('auth2', function() {
        gapi.auth2.init();
        });
}

$(document).ready(function()  {
    const userMail=Cookies.get('userMail');
    $('.mail_span').text(userMail);
    getVideos();
});

function check_member(){
    var userID=Cookies.get('userID')
    if(typeof(userID)=='undefined'){
        window.location.replace('/sign_in')
    }
}

function getVideos(){
    var userID=Cookies.get('userID')
    $.get('http://localhost:5000/teachervideos?userID='+userID, function(data, status){
        console.log(data)
        titleList=JSON.parse(data);
        var count=titleList.length
        titleList.forEach(element => {
            tableRow=$(`
                <tr>
                    <th scope="row">`+count+`</th>
                    <td>`+element.title+`</td>
                    <td>`+'http://localhost:5000/videos?videoLink='+element.title+`</td>
                    <td class='btn_td button_`+element.title+`'><button type="button" class="copy_btn btn btn-secondary">copy</button></td>
                </tr>
            `);
            tableRow.insertAfter('#title_body');
            $('.button_'+element.title).data('link','http://localhost:5000/videos?videoLink='+element.title)
            count-=1;
        });
    });
}

$(document).on('click', '.copy_btn', function(){
    var $temp = $("<input>");
    $("body").append($temp);
    $temp.val($(this).parents('.btn_td').data('link')).select();
    document.execCommand("copy");
    $temp.remove();
});

$('#inputGroupFile03').change(function(){
    file = this.files[0];
    window.formData = new FormData();
    window.formData.append(file.name,file);
    console.log(window.formData)

});

$('.submit_file').on('click',function(){
    console.log('a');
    var xhr = new XMLHttpRequest();
    xhr.addEventListener('progress', function(e) {
        var done = e.position || e.loaded, total = e.totalSize || e.total;
        console.log('xhr progress: ' + (Math.floor(done/total*1000)/10) + '%');
    }, false);
    if ( xhr.upload ) {
        xhr.upload.onprogress = function(e) {
            var done = e.position || e.loaded, total = e.totalSize || e.total;
            console.log('xhr.upload progress: ' + done + ' / ' + total + ' = ' + (Math.floor(done/total*1000)/10) + '%');
        };
    }
    xhr.onreadystatechange = function(e) {
        if ( 4 == this.readyState ) {
            console.log(['xhr upload complete', e]);
        }
    };
    xhr.open('post', "http://localhost:5000/teachervideos?userID="+Cookies.get('userID'), true);
    xhr.setRequestHeader("Content-Type","multipart/form-data");
    xhr.send(window.formData);

})
