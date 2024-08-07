import streamlit as st
from openai import OpenAI

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# 평가 기준 및 점수
evaluation_criteria = {
    "안내문 평가": {
        100: "우리 지역의 명소를 적절하게 선정하여 기존의 텍스트의 좋은 점과 부족한 점을 잘 발견하여 보완하였고 자신이 충실히 조사한 내용을 자신의 글쓰기에 반영하였으며 사회적 상호작용의 관점에서 작성된 글을 여러 번 고쳐쓰기를 통해 정련된 언어로 작성하여 제출함.",
        90: "우리 지역의 명소를 선정하여 자신이 조사한 내용을 바탕으로 보완하였고 사회적 상호작용의 관점에서 글을 여러 번 고쳐 쓰고자 노력한 흔적이 드러남.",
        80: "우리 지역의 명소에 대하여 기존 안내문을 활용하여 보완하여 수정한 결과물을 제출함.",
        70: "우리 지역의 명소를 소개하는 글을 조사한 내용을 정리하여 작성함.",
        60: "우리 지역의 명소를 소개하는 글을 작성함."
    }
}

def evaluate_text_with_gpt(text):
    prompt = f"""
    다음은 학생이 작성한 목포시 명소에 대한 안내문입니다. 이 글을 평가하고 점수를 매겨주세요.
    평가 기준은 다음과 같습니다:
    
    안내문 평가 (60-100점):
    {evaluation_criteria["안내문 평가"]}
    
    학생의 글:
    {text}
    
    평가 결과를 다음 형식으로 제공해주세요:
    안내문 평가 점수: [점수]
    피드백: [개선을 위한 구체적인 제안]
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 국어 교육 전문가이며, 학생들의 글쓰기를 평가하고 피드백을 제공하는 역할을 합니다."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

st.title("목포시 명소 안내문 작성 및 평가 시스템")

st.write("목포시의 명소에 대한 안내문을 작성해주세요. 독자를 고려하여 매력적으로 작성해보세요.")

text = st.text_area("안내문 작성", height=300)

if st.button("평가하기"):
    if text:
        evaluation_result = evaluate_text_with_gpt(text)
        st.write("### 평가 결과")
        st.write(evaluation_result)
    else:
        st.warning("안내문을 작성해주세요.")

st.write("피드백을 참고하여 안내문을 수정해보세요. 수정 후 다시 '평가하기' 버튼을 눌러 개선된 점수를 확인할 수 있습니다.")
