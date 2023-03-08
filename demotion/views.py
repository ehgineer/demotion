from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Image, Prediction
import datetime
from .tfs_api import prediction_req
import random


def index(request):
    return render(request, 'demotion/page1.html')

def upload_image(request):
    print('함수 upload_image() 호출 -', datetime.datetime.now())
    if request.method == 'POST':
        model= Image()
        model.image = request.FILES['image']
        model.date = datetime.datetime.now()
        model.name = request.POST['dogname']
        model.save()
        #print(model.image)
        #print("media/"+str(model.image))
        print('===model1-Image saved===')
        
        model2 = Prediction()
        model2.prediction = prediction_req("media/"+str(model.image))
        model2.date = datetime.datetime.now()
        model2.image = model
        model2.save()
        print('===model2-Prediction saved===')
        
        context = {'newimage': 'media/'+str(model.image)}
        return redirect('/page2/%s' % model2.id, context)
        
    return render(request, 'page1.html') 

def show_result(request, pred_id):
    print('show result 시작')
    if request.method =='GET':
        # 외래키 참조 목적 
        pred = Prediction.objects.filter(pk=pred_id)[0]
        
        image = "/media/" + str(pred.image.image)
        name = str(pred.image.name)
        
        # 화남
        if pred.prediction == "0":
            angry_list =[   "그르르르르르크르르르르르르르그르르르 {}가 화가난다!!".format(name),
                        "그르르르릉!! {}은/는 화가 잔뜩 났그르릉~~.".format(name), 
                        "그르르르르릉!! {}은/는 몹시 흥분한 상태르릉~".format(name),
                        "컹컼컹컹컹그르르컹컹 {} 크르르를컹컹".format(name),
                        "멍멍!! {}은/는 분노를 느끼고 있어요!!!".format(name)]
            angry_solution = [  "{} 눈을 마주치지 말아주세요".format(name),
                            "{} 차분하고 단호한 말로 진정시켜 주세요".format(name),
                            "{}와 거리 두기, 혼자 진정할 수 있는 시간을 만들어 주세요.".format(name),
                            "침착하고 안정적인 행동을 통해 {}가 진정할 수 있게 도와주세요.".format(name)]
            random_feeling = angry_list[random.randrange(0,  len(angry_list))]
            random_solution = angry_solution[random.randrange(0, len(angry_solution))]
        # 행복함
        elif pred.prediction == "1":
            happy_list = [  "왈왈~~~ 너무 너무 행복해~! {}은/는 주인님과 함께라면".format(name),
                        "깡총깡총! {}은/는 오늘도 행복해서 열심히 뛰어다녀야지!!".format(name),
                        "{}!! 멍멍! 멍멍! ".format(name), 
                        "멍멍! {}은/는 꼬리를 열심히 흔들어야지~~".format(name), 
                        "너무 기분좋아!! 배 들어내야지 {}이 문질러줭~~".format(name),
                        "{}, 너무 행복해서 기절!....zZZ..zzZ..".format(name),
                        "멍멍. {}은/는 주인님이 너무 좋아 품안에 안겨있을랭".format(name),
                        "{} 기분업!! 뽀뽀 ♥.♥".format(name),
                        "멍멍 {}가 아끼는 장난감 빌려줄게~~".format(name),
                        "{} 행복한 미소~~~SMILE~~~~".format(name)]
            happy_solution = [
                            "{}의 기분을 더 업 시켜주기 위해 산책을 시켜주세요!".format(name),
                            "그럼 {}가 더 귀여워 질 거에요!".format(name),
                            "{}의 배를 문질문질 해주세요!".format(name),
                            "{}의 머리를 쓰담쓰담 해주세요!".format(name),
                            "식욕이 왕성해진 {}에게 오늘은 좀 더 간식을 주세요!".format(name),
                            "{}이 핥아줄때 열심히 뽀뽀해주세요!  ♥.♥ ".format(name),
                            "{}과 장난감을 가지고 놀아주세요!".format(name),
                            "오늘은 자기시간보다 더 {}와/과 함께 보내는 시간에 더 할애해주는 건 어떨까요?".format(name),
                            "{}이 가지고 놀 수 있게 장난감을 주시면 더 행복해질 거에요".format(name),
                            "{}을 안아주세요~".format(name),
                            "{}의 아이컨택을 해주고 눈을 쳐다보면서 얘기해주세요! 교감을 할 수록 {}은/는 더 행복해진답니다".format(name, name)
        ]
            random_feeling = happy_list[random.randrange(0, len(happy_list))]
            random_solution = happy_solution[random.randrange(0, len(happy_solution))]
        # 평범함
        elif pred.prediction == "2":
            idle_list = [   "멍멍멍!! {} 따분해멍 따분해멍....-_-" .format(name),
                        "왈왈~ 왈 {} 재미없따 재미없따..왈..-_-" .format(name),
                        "머...엉 해 {} 멍멍0_0".format(name),
                        "뭉뭉!! 띠오오옹 뭉심뭉심 {} 심심해".format(name),
                        "멍멍 {} 지루해!!".format(name),
                        "머...머머멍" ,"뭉뭉 {}은/는 뭉잼없어!!+_+".format(name),
                        "멍멍멍!! {}은/는 어떻게 해야 할지 모르겠다 멍. 주인님 왜저러지? 혼란스럽다 멍".format(name),
                        "끼잉끼잉... {}은/는 누구... 여기는 어디지? 어지럽다 멍".format(name),
                        "{}은/는 주인님이 화나 보여... 어떻게 해야 화를 풀어 드릴 수 있을까? 어렵다. 왈왈".format(name),
                        "{} 힘내자 멍! 아무것도 하기 싫고 주인님도 무슨 기분인지 모르겠지만 {}가 힘내면 주인님도 좋아할거야. 멍멍 왈왈!".format(name, name),
                        "{} 밥 더 먹고싶은데... 주인님이 허락해 줄까? 어떻게 해야 더 먹을 수 있을까..? 멍멍멍 {} 밥 더주세요 멍".format(name, name),
                        "{} 큰일났다 멍... 주인님이 아끼는 화분을 깨뜨려 버렸어... {} 혼나기 싫다 멍멍 ㅠㅠ".format(name, name)]
            idle_solution = [   "{}을/를 같이 놀아주세요".format(name),
                            "{}을/를 안아주세요".format(name),
                            "{}에게 재밌는 놀이해주세요".format(name),
                            "{}에게 음악을 틀어주세요".format(name),
                            "{}와/과 동네 한바퀴 어때요?".format(name),
                            "{}을/를 쓰다듬어주세요~! -는 주인님의 손길이 필요합니다~^^".format(name),
                            "{}을/를 산책시켜주세요~! -는 산책을 통해 기분전환을 시켜줄 수 있어요 ^^".format(name),
                            "{}을/를 간식을 챙겨보세요~! 맛있는 간식을 먹으면 기분이 좋아질거에요 ^^".format(name),
                            "{}을/를 친구를 만나게 해주세요~! 친구와 함께라면 기분이 좋아질거예요 ^^".format(name)]
            random_feeling = idle_list[random.randrange(0, len(idle_list))]
            random_solution = idle_solution[random.randrange(0, len(idle_solution))]
        # 이완됨
        else:
            relaxed_list = ["지금 {}의 상태는 약간.. 졸린... 멍.....".format(name),
                        "{}은/는 지금.. 어쩐지 편안하다...".format(name),
                        "{}은/는 조금 권태롭지만 기분은 괜찮아 보인다.".format(name),
                        "지금 {}의 마음은 봄하늘 같은 하늘색.".format(name),
                        "{}은/는 약간 불만도 있지만 편안합니다.".format(name),
                        "{}은/는 산책에서 만난 친구 냄새를 생각 중입니다.".format(name),
                        "{}은/는 내일 먹을 사료맛을 생각 중입니다.".format(name),
                        "{}은/는 지나간 산책에서 본 변을 생각 중입니다.".format(name)]
            relaxed_solution=[  "{}에게 이불을 덮어주세요.".format(name),
                            "{} 이름을 불러주세요.".format(name),
                            "{} 머리를 부드럽게 쓰다듬 해주세요.".format(name),
                            "{}을/를 위해 방 공기를 환기시켜 주세요.".format(name),
                            "{} 옆에 누워보세요.".format(name),
                            "{}의 엉덩이를 두들겨 주세요.".format(name),
                            "{}에게 간식을 먹을 건지 물어보세요.".format(name),
                            "{}을/를 위해 방의 조명을 조금 낮춰줍시다.".format(name),
                            "{}가 변을 볼 수 있게 산책을 같이 나가봅시다.".format(name)]
            random_feeling = relaxed_list[random.randrange(0, len(relaxed_list))]
            random_solution = relaxed_solution[random.randrange(0, len(relaxed_solution))]
        context = {'image': image, 'feeling': random_feeling, 'solution': random_solution, 'name' : name}
        return render(request, 'demotion/page2.html', context)
    else:
        print('error occurred')
        return False
    