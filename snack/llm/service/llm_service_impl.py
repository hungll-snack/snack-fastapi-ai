from openai import OpenAI
import os
from rag.embedder import get_embedding
from rag.faiss_index import search

class LLMServiceImpl:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            timeout=10  # ✅ 여기서 timeout 설정
        )

    def get_response_from_openai(self, prompt: str) -> str:
        #rag
        query_embedding = get_embedding(prompt)
        similar_restaurants = search(query_embedding)

        extra_context = "\n".join([
            f"{r['name']} ({r['address']}) 평점: {r['rating']}" for r in similar_restaurants
        ])
        #여기부턴 prompt
        prompt += f"\n📍 관련 맛집 정보:\n{extra_context}"

        print(f"🔍 프롬프트:\n{prompt}")
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                stream=True
            )
            result = response.choices[0].message.content
            print(f"✅ 응답 결과: {result}")
            return result
        except Exception as e:
            print(f"❌ OpenAI 호출 실패: {e}")
            return "미안해요! 헝글이 딱맞는 대답을 찾기위해 알아보고있어요 💡"
