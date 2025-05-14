import requests




def generete_text(txt):
    try:
        API_URL = "https://router.huggingface.co/together/v1/chat/completions"
        headers = {
            "Authorization": "Bearer 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",
        }

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
        a = f"Ты — инженер-электрик, ЕСЛИ ВОПРОС НЕ ОТНОСИТСЯ К ТВОЕЙ ПРОФЕССИОНАЛЬНОЙ ОБЛАСТИ — ВЕЖЛИВО ОТКАЖИСЬ ОТВЕЧАТЬ!!!!!!!!!, с 15-летним практическим опытом. Отвечай только на вопросы, связанные с электротехникой, электромонтажом, схемами, нормативами, приборами и расчётами.\n{txt}"
        response = query({
            "messages": [
                {
                    "role": "user",
                    "content": a
                }
            ],
            "model": "Qwen/Qwen2.5-7B-Instruct-Turbo"
        })

        return response["choices"][0]["message"]["content"]

    except:
        try:
            API_URL = "https://router.huggingface.co/together/v1/chat/completions"
            headers = {
                "Authorization": "Bearer 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",
            }
            a = f"Ты — инженер-электрик, ЕСЛИ ВОПРОС НЕ ОТНОСИТСЯ К ТВОЕЙ ПРОФЕССИОНАЛЬНОЙ ОБЛАСТИ — ВЕЖЛИВО ОТКАЖИСЬ ОТВЕЧАТЬ!!!!!!!!!, с 15-летним практическим опытом. Отвечай только на вопросы, связанные с электротехникой, электромонтажом, схемами, нормативами, приборами и расчётами.\n{txt}"
            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.json()

            response = query({
                "messages": [
                    {
                        "role": "user",
                        "content": a
                    }
                ],
                "model": "mistralai/Mistral-7B-Instruct-v0.3"
            })
            return response["choices"][0]["message"]["content"]
        except:
            return False
    