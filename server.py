from websockets.sync.server import serve
import requests
url = "https://api.intelligence.io.solutions/api/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6ImRmNmY5NDhlLWVjNWYtNDkyOC1iOWUwLWJmMTBkYTQ5YzFlZiIsImV4cCI6NDkwNzM5NzIwMH0.FPioRMvnw4n8A12Y_pEPVwagXgZh08CdsJcjy2BjL16GDqSOvqwB0thNLRVj2eVjGU3F7Y23k3b2bEfQnDl6Ig"
}


def ai_answer(message):
    data = {  
    "model": "deepseek-ai/DeepSeek-R1-0528",
    "messages": 
    [
        {
            "role": "system",
            "content": "You are a helpful assistant"
        },
        {
            "role": "user",
            "content": message
        }
    ]
    }

    response = requests.post(url, headers=headers, json=data)
    data = response.json()

    text = data['choices'][0]['message']['content']

    parts = text.split('</think>')
    answer = parts[-1].strip()

    return answer 


def handle_client(websocket):
    try:
        while True:
            message = websocket.recv()
            print(f"Получено: {message}")

            question = message[4:].strip()
            
            response = ai_answer(question)
            websocket.send(response)
                
    except Exception as e:
        print(f"Ошибка соединения: {e}")


with serve(handle_client, "localhost", 8000) as server:
    print("Сервер запущен на ws://localhost:8000")
    server.serve_forever()