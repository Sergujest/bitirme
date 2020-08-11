from AnswerClass import *
from QuestionClass import *
from LikeClass import *
from UserClass import *

#like=Like(False,'5ef103f8a66227f987935860','5ef3dbbef51aed20ee5adeaf')
#like.insertLikeToQuestionByQuestionID('5ef3c3dde44358dba3aab5b1')
#like.updateAnswerLikeByQuestionIDAndAnswerID('5ef3c3dde44358dba3aab5b1','5ef3db037b605785481ac4e8')
#like.insertLikeToAnswerByQuestionIDAndAnswerID('5ef3c3dde44358dba3aab5b1','5ef3dec5726af95a59436cc0')
#Like.deleteAnswerLikeByIDQuestionIDAndAnswerID('5ef3dbbef51aed20ee5adeaf','5ef3c3dde44358dba3aab5b1','5ef3dec5726af95a59436cc0')

#answer=Answer('5ef103f8a662255555935890','veli@gmail.com','Gittik Gideli',5,_id='5ef3db037b605785481ac4e8')
#answer.updateAnswerDetailByQuestionID('5ef3c3dde44358dba3aab5b1')
#answer.insertAnswerByQuestionID('5ef3c3dde44358dba3aab5b1')
#Answer.deleteAnswerByIDAndQuestionID('5ef3dab7109c21283f2cfd40','5ef3c3dde44358dba3aab5b1')

#question=Question('5ef103f8a66227f98793587a','1@a','a','a','a','a',5)
#question.insertQuestion()
print(Question.getQuestionsByVideoAndTime('excel',65))
#user=User('ali','ali@a')
#user.insertUser()