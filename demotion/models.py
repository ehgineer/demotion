from django.db import models
# import jsonfield  # json 데이터를 데이터베이스에 저장하기 위한 라이브러리


# 1. 이미지 저장 테이블
# 컬럼: 이미지 업로드 날짜시간, 이미지 파일 경로(/media/ … )
class Image(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(null=True)
    image = models.ImageField(upload_to="")
    
    # def __str__(self):
    #    return self.name
    
# 2. 예측 결과와 이미지 묶어 저장하는 테이블
# 컬럼: 예측 날짜시간, 이미지 인덱스(외래키), 예측 결과
class Prediction(models.Model):
    date = models.DateTimeField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    prediction = models.CharField(max_length=255)

    # def __str__(self):
    #    return self

# 3. 결과에 맞춰 내보낼 해석 저장해둘 테이블
# 컬럼: 해석이름, 해석 내용
class Interpretation(models.Model):
    name = models.ForeignKey(Image, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)

    # def __str__(self):
    #    return self.description