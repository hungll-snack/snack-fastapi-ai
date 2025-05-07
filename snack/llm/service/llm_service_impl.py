from openai import OpenAI
import os

class LLMServiceImpl:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=10  # ✅ 여기서 timeout 설정
        )

    def get_response_from_openai(self, prompt: str) -> str:
        print(f"🔍 프롬프트:\n{prompt}")
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            result = response.choices[0].message.content
            print(f"✅ 응답 결과: {result}")
            return result
        except Exception as e:
            print(f"❌ OpenAI 호출 실패: {e}")
            return "미안해요! 헝글이 딱맞는 대답을 찾기위해 알아보고있어요 💡"
