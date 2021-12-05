import requests
import json
import re
from sentence_transformers import SentenceTransformer, util
import numpy as np
import random
from django.shortcuts import render
from konlpy.tag import Kkma
import math
from operator import itemgetter
from nltk.tokenize import word_tokenize


models = SentenceTransformer('distiluse-base-multilingual-cased-v1')

#데이터 전처리
def process(info, sim):
    input_sim = sim  # input data 유사성 민감도 지정 / 숫자가 작을수록 관련 없는게 나올 확률이 커짐 / 최소 50이상 설정
    input_text = info
    input_text_list = input_text.split(' ')  # input data 띄어쓰기로 나누기
    eng_text = re.sub('[^a-zA-z]', ' ', input_text).strip()
    # print(word_tokenize(input_text))
    # print(input_text_list)

    kkma = Kkma()  # 꼬마를 작용시 분모가 중복 되는 경우가 생김, 이를 제거해야 함
    copy = []
    for txt in input_text_list:
        txt_ = kkma.nouns(txt)
        # print(txt_)

        if len(txt_) > 1:  # (명사가 쪼개졌을 경우)
            max_string = max(txt_, key=len)  # 가장 긴 값을 제거 (중복값)
            txt_.remove(max_string)

        copy += txt_
    # print(copy)

    if len(copy) > 3:
        del_list = []
        for i in range(math.ceil(len(copy) - 2)):
            overlap_txt = ''.join(
                (itemgetter(i, i + 2)(copy)))  # abc를 kkma로 쪼갤 경우 =>  a, ab, abc, b, c => abc 제거 => ab를 제거하는 과정
            if overlap_txt in copy:
                del_list.append(overlap_txt)
                # print(del_list)
        [i for i in del_list if not i in copy or copy.remove(i)]  # 차집합인데 순서가 안 바뀜
    text = ' '.join(copy)

    if input_sim > 45:
        text += ','  # ,를 넣을 경우 강제로 기업설명으로 인식시켜서 조금 더 제한적인 슬로건 등장

    # 영어 슬로건이 포함 된 경우 초기상태로
    if eng_text:
        if eng_text in input_text:
            text = input_text

    return text

def ko_api(text):
    r = requests.post(
        'https://train-8dgtlge21881yafjrqb4-gpt2-train-teachable-ainize.endpoint.ainize.ai/predictions/gpt-2-ko-small-finetune', #슬로건 , 없는 정제된 5에포크
        headers = {'Content-Type' : 'application/json'
                   },
        data=json.dumps({
      "text": text,
      "num_samples": 50,
      "length":20
        }))

    #슬로건 추가
    slogan_list = []
    for slogan in r.json():
        slogan = slogan.split('\n')[0]
        slogan = slogan.split(',')[1:]
        slogan = ', '.join(slogan)
        if slogan :
          slogan_list.append(slogan)
          #print(slogan)
    #print(len(slogan_list),'개 완료')
    return slogan_list

#차집합 함수
def differ_sets(a,b) :
    lst = list(set(a) - set(b))
    return lst

# 영어 슬로건 따로 추출
def differ(slogan_list):
    eng_list = []
    slogan_list = slogan_list
    for slogan in slogan_list:
        slogan_ = re.sub('[^A-Za-z가-힣]', '', slogan)  # 영어 한글만 남기기
        slogan_ = re.sub('[^가-힣]', ' ', slogan_)  # 한글이 있으면 공백 채우기
        if slogan_.isspace():  # isalpha()는 영어 또는 한글 유무를 찾아서 안 됨
            eng_list.append(slogan)

    #print(eng_list)

    # 차집합
    kor_list = differ_sets(slogan_list, eng_list)  # 한국 슬로건만 있는 리스트
    return kor_list


# 문장 유사도
def extraction(kor_list, sim):
    # 모델 불러오기
    model = models

    # 유사도 비교할 리스트
    corpus = kor_list
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

    # 비교할 슬로건 선택
    no_sim_list = []  # 관련 없는 슬로건 추출
    total_slogan = []  # 슬로건 전체를 담는 리스트 / 중첩리스트용
    n = 0
    try:  # n이 증가하지 않을 경우 무한루프?
        while n < 4:
            # 유사도 비교할 리스트
            corpus = kor_list
            corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

            # 유사도 비교할 문장
            query = random.sample(kor_list, 1)
            kor_list = differ_sets(kor_list, query)  # kor_list에서 query를 제거

            # 코사인 유사도 사용하여 5개 유사한 슬로건 찾기
            top_k = 6  # query 포함 top 5개
            query_embedding = model.encode(query, convert_to_tensor=True)
            cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
            cos_scores = cos_scores.cpu()
            top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]  # np 사용 이유 : 순위를 순서대로 맞추기 위함

            # 민감도 비교하기 위한 유사도 더하기
            sum = 0
            for idx in top_results[1:top_k]:
                sum += cos_scores[idx]
            f_sum = float(sum) / 5  # tensor to float

            # 사용자 인풋 민감도 비교
            sim_list = []  # 유사 슬로건 담을 리스트
            if f_sum >= sim / 100:
                for idx in top_results[0:top_k - 2]:
                    sim_list.append(corpus[idx].strip())
                total_slogan.append(sim_list)
                kor_list = differ_sets(kor_list, sim_list)
                n += 1
                # print(len(kor_list))

            else:
                no_sim_list.append(query)

    except:
        pass


    return total_slogan