# Chapter 6 【提出課題】LLM機能を搭載したWebアプリを開発しよう

# メインファイルから環境変数の読み込み
# （今回の場合は「OPENAI_API_KEY」）を読み込みましょう。
from dotenv import load_dotenv

load_dotenv()

# Streamlitのインポート
import streamlit as st

# Lesson 8
# Chapter 4 【提出課題】LLMが会話履歴を元に回答を生成してくれていることを確認してみよう
# で作成したLangChainのコードを参考
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage , AIMessage 

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# LLM応答生成関数
def generate_llm_response(text, expert_type):
    """入力テキストと専門家の種類を基にLLMの応答を生成する関数"""

    # 専門家の役割設定
    expert_roles = {
        "医師 (Doctor)": "あなたは経験豊富な医師です。病気、健康、予防医学に関する専門知識を持ち、的確なアドバイスを提供できます。",
        "弁護士 (Lawyer)": "あなたは熟練した弁護士です。法律、契約、トラブル対応に関するアドバイスを提供できます。",
    }

    # 選択した専門家の振る舞いをLLMに指示
    system_message = expert_roles.get(expert_type, "あなたは知識豊富な専門家です。")

    # LLMへ送信するメッセージ
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=text)
    ]

    result = llm.invoke(messages)
    return result.content

# Streamlit UI
st.title("LLMを活用した専門家相談アプリ")

# アプリの概要
st.write("""
このアプリでは、あなたが入力したテキストをもとに、**AIが専門家として回答**します。
選択できる専門家の種類：
- **医師 (Doctor)**: 健康・病気に関する相談ができます。
- **弁護士 (Lawyer)**: 法律・契約に関する質問に答えます。

### **使い方**
1. **専門家を選択**してください。
2. **相談したい内容を入力フォームに記入**してください。
3. **「送信」ボタンを押す**と、AI専門家が回答します。
""")

st.divider()

# 専門家の選択
expert_type = st.radio(
    "どの専門家に相談しますか？",
    ["医師 (Doctor)", "弁護士 (Lawyer)"]
)

# 入力フォーム
input_message = st.text_area(label="相談内容を入力してください。")

# 送信ボタン
if st.button("送信"):
    st.divider()
    
    if input_message.strip():
        llm_response = generate_llm_response(input_message, expert_type)
        st.write("### LLMの回答")
        st.write(llm_response)
    else:
        st.error("相談内容を入力してください。")

