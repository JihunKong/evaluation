import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

# NLTK 데이터 다운로드
nltk.download('punkt')
nltk.download('stopwords')

# 평가 기준 및 점수
evaluation_criteria = {
    "글로컬 글쓰기의 과정 평가": {
        100: "쓰기의 전 과정에서 산출된 결과물을 체계용 포트폴리오로 정리하였으며 그 과정에서 동료들과 나눈 피드백을 충실히 고려하였을 뿐만 아니라 스스로도 동료들을 위해 발전적인 피드백을 제공하였음.",
        90: "쓰기의 전 과정에서 산출된 결과물을 체계용 포트폴리오로 정리하였으며 동료들과 나눈 피드백을 고려하였으며 적절한 피드백을 동료에게 제공함.",
        80: "쓰기의 전 과정에서 산출된 결과물을 정리하였으며 피드백을 서로 주고 받으며 글쓰기에 반영하는 모습이 나타남.",
        70: "쓰기의 과정에서 다양한 산출물을 나타내었으며 타인의 글에 피드백을 남김.",
        60: "쓰기의 과정에 따라 글쓰기를 진행한 모습이 관찰됨."
    },
    "글로컬 글쓰기의 결과물 평가": {
        100: "우리 지역의 명소를 적절하게 선정하여 기존의 텍스트의 좋은 전과 부족한 점을 잘 발견하여 보완하였고 자신이 충실히 조사한 내용을 자신의 글쓰기에 반영하였으며 사회적 상호작용의 관점에서 작성된 글을 여러 번 고쳐쓰기를 통해 정련된 언어로 작성하여 제출함.",
        90: "우리 지역의 명소를 선정하여 자신이 조사한 내용을 바탕으로 보완하였고 사회적 상호작용의 관점에서 글을 여러 번 고쳐 쓰고자 노력한 흔적이 드러남.",
        80: "우리 지역의 명소에 대하여 기존 안내문을 활용하여 보완하여 수정한 결과물을 제출함.",
        70: "우리 지역의 명소를 소개하는 글을 조사한 내용을 정리하여 작성함.",
        60: "우리 지역의 명소를 소개하는 글을 작성함."
    }
}

def evaluate_text(text):
    # 간단한 평가 로직 (실제 구현에서는 더 복잡한 NLP 기술을 사용할 수 있습니다)
    words = word_tokenize(text.lower())
    word_count = len([word for word in words if word not in stopwords.words('english')])
    
    process_score = 60
    result_score = 60
    
    if word_count > 100:
        process_score = 80
        result_score = 80
    if word_count > 200:
        process_score = 90
        result_score = 90
    if word_count > 300 and re.search(r'목포|명소|관광|역사|문화', text):
        process_score = 100
        result_score = 100
    
    return process_score, result_score

def get_feedback(score):
    if score >= 90:
        return "훌륭한 글입니다! 더 나은 글을 위해 추가적인 세부 정보나 독자의 관심을 끌 수 있는 흥미로운 사실을 포함해보세요."
    elif score >= 80:
        return "좋은 글입니다. 목포의 특징을 더 자세히 설명하고, 독자가 방문하고 싶어지도록 설득력 있게 작성해보세요."
    elif score >= 70:
        return "기본적인 내용은 잘 작성되었습니다. 목포의 독특한 매력을 더 강조하고, 구체적인 예시를 들어 설명해보세요."
    else:
        return "글의 구조와 내용을 더 발전시켜 보세요. 목포의 주요 명소, 역사, 문화적 특징 등을 포함하여 더 풍부한 내용으로 만들어보세요."

st.title("목포시 명소 안내문 작성 및 평가 시스템")

st.write("목포시의 명소에 대한 안내문을 작성해주세요. 독자를 고려하여 매력적으로 작성해보세요.")

text = st.text_area("안내문 작성", height=300)

if st.button("평가하기"):
    if text:
        process_score, result_score = evaluate_text(text)
        
        st.write("### 평가 결과")
        st.write(f"글로컬 글쓰기의 과정 평가 점수: {process_score}")
        st.write(evaluation_criteria["글로컬 글쓰기의 과정 평가"][process_score])
        st.write(f"글로컬 글쓰기의 결과물 평가 점수: {result_score}")
        st.write(evaluation_criteria["글로컬 글쓰기의 결과물 평가"][result_score])
        
        st.write("### 피드백")
        st.write(get_feedback(min(process_score, result_score)))
    else:
        st.warning("안내문을 작성해주세요.")

st.write("피드백을 참고하여 안내문을 수정해보세요. 수정 후 다시 '평가하기' 버튼을 눌러 개선된 점수를 확인할 수 있습니다.")
