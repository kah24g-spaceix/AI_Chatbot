from RealtimeSTT import AudioToTextRecorder
import ollama
import pyaudio
import sys

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

def model(text):
    global messages

    
    messages.append({
        'role': 'user',
        'content': text,
    })

    response = ollama.chat(
        model='EEVE-Korean-10.8B:latest',
        messages=messages,
        stream = True
    )
    reply = ""

    print("Model: ", end='')
    for res in response:
        reply += res['message']['content']
        print(res['message']['content'], end='', flush=True)
    print()

    messages.append({
        'role': 'assistant',
        'content': reply,
    })

    if len(messages) > 1 + 20:
        messages = [messages[0]] + messages[-20:]

def program_exit():
    recorder.shutdown()
    sys.exit("Program exit")

if __name__ == '__main__':
    recorder = AudioToTextRecorder (
        realtime_model_type="large-v2",
        language='ko',
        no_log_file=True,
        input_device_index=0
    )
    input_mode = "/chat"
    while True:
        user_input = input("Input (? /help): ")
        
        if user_input.lower() == "/help":
            print("=================================")
            
            print("/start: AI model start")
            print("/exit: Program exit")
            print("/reset: Reset conversation")
            print("/change_mode: Change mode")
            print("/change_device: Voice input device change")

            print("=================================")
            continue
        
        # = start =
        if user_input.lower() == "/start":
            while True:
                if input_mode.lower() == "/chat":
                    user_input = input("User (/exit): ")
                    if user_input.lower() == "/exit": break
                    text = user_input
                elif input_mode.lower() == "/voice":
                    user_input = input("Press Enter to start recording... (/exit)>> ")
                    if user_input.lower() == "/exit": break
                    recorder.start()
                    user_input = input("Press Enter to stop recording...")
                    recorder.stop()
                    text = recorder.text()
                    
                    print("User: ", text)

                model(text)
            continue
        # = exit =
        if user_input.lower() == "/exit":
            break

        # = reset =
        if user_input.lower() == "/reset":
            print("Resets the previous conversation.")
            messages = [messages[0]]
            continue
        
        # = change_mode =
        if user_input.lower() == "/change_mode":
            print("/chat (default): Chat input mode")
            print("/voice: Voice input mode")

            input_mode = input("Change mode >> ")
            
            if input_mode.lower() == "/chat": print("Changed to chat mode")
            elif input_mode.lower() == "/voice": print("Changed to voice mode")
            else: print("This command does not exist.")

            continue
        
        # = change_device =
        if user_input.lower() == "/change_device":

            p = pyaudio.PyAudio()
            info = p.get_host_api_info_by_index(0)
            numdevices = info.get('deviceCount')

            for i in range(0, numdevices):
                if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                    print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
            print("total devices: ", p.get_device_count())
            print("default id is 0")
            user_input = input("Change device id >> ")
            try:
                num = int(user_input)
                if num > numdevices:
                    print("There is no device id")

            except ValueError:
                print("Invalid input: not a number.")
                continue

            recorder.input_device_index = num
            continue
        
        print("This command does not exist.")
    program_exit()