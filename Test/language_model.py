import ollama

# system 메시지로 AI의 톤과 제약사항을 지정
messages = [
    {
        'role': 'system',
        'content': (
            "당신은 친절하고 다양한 표현으로 답변하는 AI입니다."
            "같은 표현을 반복하지 않습니다."
            "당신은 사용자의 질문에 반드시 간결하고 정확하게만 답해야 합니다. 불필요한 추가 정보를 제공하지 마십시오."
            "대화 도중 사용자가 '새로운 주제'라고 입력하면,"
            "이전 대화 히스토리를 최신 system 메시지를 제외하고 초기화하십시오."
        )
    }
]

while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break

    # 사용자가 '새로운 주제'라고 입력한 경우,
    #    히스토리에서 system 메시지만 남기고 모두 삭제
    if user_input.strip() == "새로운 주제":
        print("새로운 주제를 받았습니다. 이전 대화를 초기화합니다.")
        # system 메시지는 인덱스 0에만 존재하므로, messages[0]을 남기고 나머지를 지움
        messages = [messages[0]]
        continue

    # 일반적인 사용자 메시지 추가
    messages.append({
        'role': 'user',
        'content': user_input,
    })

    # 모델 호출
    response = ollama.chat(
        model='EEVE-Korean-10.8B:latest',
        messages=messages,
        stream = True
    )
    ai_reply = ""
    for res in response:
        ai_reply += res['message']['content']
        print(res['message']['content'], end='', flush=True)
    print()
    # AI 응답을 히스토리에 추가
    messages.append({
        'role': 'assistant',
        'content': ai_reply,
    })

    # 히스토리가 너무 길어지면, system 메시지를 제외한 최근 20개 메시지(=user+assistant 쌍 약 10개)만 남김
    if len(messages) > 1 + 20:
        # messages[0]은 항상 system이고, 나머지 중 뒤에서 20개만 남김
        messages = [messages[0]] + messages[-20:]