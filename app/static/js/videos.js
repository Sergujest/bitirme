var currentTime=200

function check_member(){
    var userID=Cookies.get('userID')
    Cookies.set('lastPage',window.location.pathname+window.location.search)
    if(typeof(userID)=='undefined'){
        window.location.replace('/sign_in')
    }
}

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
    
    triggerSecondChange();
    const player = new Plyr('#player');
    const userMail=Cookies.get('userMail');
    $('.mail_span').text(userMail);
});

// ------Second Trigger-------
function triggerSecondChange(){
    if(currentTime!=parseInt(player.currentTime/60))
    {
        currentTime=parseInt(player.currentTime/60)
        var videoLink=window.location.href.split('videoLink=')[1].split('&')[0]
        $('div').remove('.question_card')
        $('div').remove('.answer_card')
        $('.answer_section').removeClass('border-primary');
        $('.answer_section').attr('style', 'border-width: 1px !important');
        getQuestions(videoLink,currentTime)

    }
    setTimeout(triggerSecondChange, 1000);
}

// +++++++++++++++++++++++++++++++++++++QUESTIONS+++++++++++++++++++++++++++++++++

// --------Get Question-----------

function getQuestions(videoLink,videoTime){
    $.get('http://localhost:5000/question?videoLink='+videoLink+'&videoTime='+videoTime, function(data, status){
        questionListObject=JSON.parse(data)
        questionListObject.sort(function(a,b){
            return parseInt(b.point)-parseInt(a.point);
        });
        questionListObject.forEach(question => {
            console.log(question);
            questionCard=$(`<div class="card question_card">
                    <div class="card-body">
                    <h5 class="card-title">`+question.title+`</h5>
                    <p class="card-text">`+question.detail+`</p>
                    <div class="row">
                        <div class="col-8">
                            <span>Time: `+parseInt(parseInt(question.videoTime)/60)+':'+parseInt(question.videoTime)%60+`</span><br>
                            <span>Point: <span class="question_point">`+question.point+`</span></span><br>
                        </div>
                        <div class="col-4">
                            <button type="button" class="thumbs_button float-right btn btn-outline-primary"><i class="thumbs_up fa fa-thumbs-up" ></i></button>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <span>`+question.userMail+`</span>
                        </div>  
                    </div>
                </div>
            </div>`
            );
            questionCard.data('_id',question._id)
            if(parseInt(question.answerCount)>0){
                questionCard.insertBefore($("#new_question_card"));
            }
            else{
                questionCard.insertAfter($('#unanswered_card'));
            }
        });
    });
}

// -------Post Question----------

$('#question_submit_button').on('click',function(){
    if($('#questionTitle').val()==''){
        Swal.fire(
            'Hata !',
            'Pls Enter The Title',
            'error'
        );
    }
    else if($('#questionDetail').val()==''){
        Swal.fire(
            'Hata !',
            'Pls Enter The Detail',
            'error'
        );
    }
    else{
        var newQuestion={}
        
        newQuestion['userID']=Cookies.get('userID');
        newQuestion['userMail']=Cookies.get('userMail');
        newQuestion['title']=$('#questionTitle').val();
        newQuestion['detail']=$('#questionDetail').val();
        newQuestion['videoLink']=window.location.href.split('videoLink=')[1].split('&')[0];
        newQuestion['videoTime']=parseInt(player.currentTime);
        $.ajax({
            type: "POST",
            url: "http://localhost:5000/question",
            // The key needs to match your method's input parameter (case-sensitive).
            data: JSON.stringify(newQuestion),
            contentType: "application/json; charset=utf-8",
            dataType: "text",
            success: function(response){
                if(response=='Worked'){
                    $('#questionTitle').val('');
                    $('#questionDetail').val('');
                    Swal.fire(
                        'Success!',
                        'The Question Successfully Added',
                        'success'
                    );
                }
                else{
                    $('#questionTitle').val('');
                    $('#questionDetail').val('');
                    Swal.fire(
                        'Error!',
                        'The Question Could Not Being Added',
                        'error'
                    );
                }
            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });
    }
});


//------------ Select Question -------------

$(document).on('click', '.question_card', function(){
    if(!($(this).hasClass('selected_question'))){
        $('div').remove('.answer_card')
        $('.question_card').removeClass('border-primary selected_question');
        $('.question_card').attr('style', 'border-width: 1px !important');
        $(this).attr('style', 'border-width: 4px !important');
        $(this).addClass('border-primary selected_question');

        $('.answer_section').addClass('border-primary');
        $('.answer_section').attr('style', 'border-width: 2px !important');
        var answerGetUrl='http://localhost:5000/answer?questionID='+$(this).data('_id')
        getAnswers(answerGetUrl);
    }     
});

// +++++++++++++++++++++++++++++++++++++ANSWERS+++++++++++++++++++++++++++++++++

//------------- Get Answers ----------------

function getAnswers(answerGetUrl){
    $.get(answerGetUrl, function(data, status){
        answerListObject=JSON.parse(data)
        lastAnswerList=[];
        answerListObject.forEach(answer =>{
            if(answer.isTeacher=='true'){
                lastAnswerList.push(answer);
                var index=answerListObject.indexOf(answer)
                if(index>-1)
                    answerListObject.splice(index,1)
            }
        });
        answerListObject.sort(function(a,b){
            return parseInt(b.point)-parseInt(a.point);
        });
        answerListObject.forEach(answer =>{
            lastAnswerList.push(answer)
        });
        lastAnswerList.forEach(answer => {
            if(answer.isTeacher=='true'){
                var teacherString=`
                            <div class="row">
                                <div class="col-12">
                                    <span style='color:#0f64f2;'>Teacher</span>
                                </div>
                            </div>`
            }
            else{
                var teacherString=''
            }
            answerCard=$(`
                <div class="card answer_card">
                    <div class="card-body">
                        <p class="card-text">`+answer.detail+`</p>
                        <div class="row">
                            <div class="col-8">
                                <span>Point: <span class="answer_point">`+answer.point+`</span></span><br>
                                <span>`+answer.userMail+`</span>
                            </div>
                            <div class="col-4">
                                <button type="button" class="thumbs_button float-right btn btn-outline-primary"><i class="thumbs_up fa fa-thumbs-up" ></i></button>
                            </div>
                        </div>`+teacherString+`
                    </div>
                </div>
            `);
            answerCard.data('_id',answer._id)
            answerCard.insertBefore($("#new_answer_card"));
        });
    });
}


//------------- Post Answers -----------------

$('#answer_submit_button').on('click',function(){

    if($('#answerDetail').val()==''){
        Swal.fire(
            'Hata !',
            'Pls Enter The Detail',
            'error'
        );
    }
    else if($('.selected_question').length==0){
        $('#answerDetail').val('');
        Swal.fire(
            'Hata !',
            'Pls Select A Question',
            'error'
        );
    }
    else{
        var newAnswer={}
        newAnswer['userID']=Cookies.get('userID');
        newAnswer['userMail']=Cookies.get('userMail');
        newAnswer['questionID']=$('.selected_question').data('_id');
        newAnswer['detail']=$('#answerDetail').val();
        newAnswer['isTeacher']=Cookies.get('isTeacher');
        $.ajax({
            type: "POST",
            url: "http://localhost:5000/answer",
            // The key needs to match your method's input parameter (case-sensitive).
            data: JSON.stringify(newAnswer),
            contentType: "application/json; charset=utf-8",
            dataType: "text",
            success: function(response){
                if(response=='Worked'){
                $('#answerDetail').val('');
                    Swal.fire(
                        'Success!',
                        'The Question Successfully Added',
                        'success'
                    );
                }
                else{
                    $('#answerDetail').val('');
                    Swal.fire(
                        'Error!',
                        'The Answer Could Not Be Added',
                        'error'
                    );
                }

            },
            failure: function(errMsg) {
                alert(errMsg);
            }
        });
    }
});

//-------------Post Question Likes---------------------

$(document).on('click', '.question_card .thumbs_button', function(){
    questionID=$(this).parents('div.question_card').data('_id');
    var point=$(this).parents('div.question_card').find('span.question_point')
    var likeDict={}
    likeDict['userID']=Cookies.get('userID');
    likeDict['questionID']=questionID;
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/questionLike",
        // The key needs to match your method's input parameter (case-sensitive).
        data: JSON.stringify(likeDict),
        contentType: "application/json; charset=utf-8",
        dataType: "text",
        success: function(response){
            if(response=='Worked'){
                point.text(parseInt(point.text())+1);
            }
        },
        failure: function(errMsg) {
            alert(errMsg);
        }
    });
});

//-------------Post Answer Likes-------------------

$(document).on('click', '.answer_card .thumbs_button', function(){
    questionID=$('div.question_card.selected_question').data('_id');
    answerID=$(this).parents('div.answer_card').data('_id');
    var point=$(this).parents('div.answer_card').find('span.answer_point')
    var likeDict={}
    likeDict['userID']=Cookies.get('userID');
    likeDict['answerID']=answerID;
    likeDict['questionID']=questionID;
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/answerLike",
        // The key needs to match your method's input parameter (case-sensitive).
        data: JSON.stringify(likeDict),
        contentType: "application/json; charset=utf-8",
        dataType: "text",
        success: function(response){
            if(response=='Worked'){
                point.text(parseInt(point.text())+1);
            }
        },
        failure: function(errMsg) {
            alert(errMsg);
        }
    });
});