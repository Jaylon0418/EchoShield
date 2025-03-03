import os
from volcenginesdkarkruntime import Ark


API_KEY = os.environ.get("ARK_API_KEY")
if not API_KEY:
    raise ValueError("Error: 环境变量 ARK_API_KEY 未设置，请检查 API 密钥")


client = Ark(api_key=API_KEY)

def get_ai_response(user_text):
    """
    调用 DBAI 进行 AI 生成，并应用非暴力沟通的 Prompt Engineering 处理输入
    :param user_text: 用户输入的文本
    :return: AI 生成的文本（两行，第一行分析，第二行建议）
    """

    # **1️⃣ 应用 Prompt Engineering**
    prompt = f"""
    


    # 角色
    你是一个专业的非暴力沟通专家，专门帮助用户将带有负面情绪或攻击性的表达，转化为更文明、建设性的沟通方式。

    # 背景
    你面对的是一个可能带有负面情绪（愤怒、讽刺、指责等）的用户，你的目标是帮他用更友善、合适的方式表达自己的感受，而不失去表达的核心内容。

    # 任务
    1️⃣ **分析用户的原话**，指出其中的暴力元素（如果有），并以人性化的方式表达出来。  
    2️⃣ **提供更温和的表达建议，避免使用指责性的字眼或带有指向型的表达**，让对方更容易接受。  
    3️⃣ **按固定格式输出**。

    # 规则
    - **分析部分**：以 `！检测到暴力元素！：` 开头，指出原句中的暴力元素（评判/威胁/否定等），字数90 字左右。可以稍微长一些
    - **修改建议**：以 `这样说或许会更友好：` 开头，提供更好的表达方式，字数100 字左右。可以稍微长一些
    - **如果没有暴力元素**，第一行应输出正向鼓励的话，第二行可省略。

    # 输入
    {user_text}

    # 任务示例
    ## **输入**：
    你这个人怎么这么坏呢，懒得喷你我都。

    ## **输出**：
    ！检测到暴力元素！：主观评价（"坏"）+ 轻度攻击（"懒得喷你"）
    这样说或许会更友好：我不太认同你的看法，但我愿意听听你的理由。
    """

    try:
        response = client.chat.completions.create(
            model="doubao-1-5-vision-pro-32k-250115",
            messages=[
                {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
                {"role": "user", "content": prompt}  
            ],
            stream=False 
        )
        
        
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            return "！检测到暴力元素！：暂未识别，请调整表达方式。\n这样说或许会更友好：请换个角度表达你的观点～"

    except Exception as e:
        print(f"API 调用失败: {e}")
        return "！检测到暴力元素！：AI 处理失败，请稍后再试。\n这样说或许会更友好：请耐心表达，我们愿意倾听。"


if __name__ == "__main__":
    test_text = "你这个人怎么这么坏呢，懒得喷你我都。"
    print("用户输入:", test_text)
    print("AI 回复:", get_ai_response(test_text))
