import requests
#import json

# mieć zdefiniowaną tę funkcję, którą da się zaimportować
def define_technical_contradiction(problem_description: str) -> dict:
    url = "http://loclahost:11434/v1/api/chat"
    system_message = """
    Twoje zadanie poleg ana tym, żeby przeformułować opis problemu podany przez użytkownika
    do postaci sprzeczności technicznej wg TRIZ.
    
    <context>
    Sprzeczność techniczna polega na tym, że wykonując jakieś działanie, prowadzimy
    do wywołania pozytywnej i negatywnej konsekwencji. Na przykład, zwiększając
    grubość przekroju zwiększymy wytrzymałość belki, ale też zwiększymy jej masę.
    </context>
    
    <przykłady>
    USER: Jeśli zwiększę grubośc belki zwiększę jej wytrzymałość, ale zwiększę też masę belki
    AI:
        action: zwiększenie grubości przekroju
        positive_effect: zwiększenie wytrzymałości
        negative_effect: zwiększenie masy
    </przykłady>
    
        
    """
    messages = [
        {'role' : "system", 
        "content": system_message
        }, 
        {'role':'user', 
        'content': problem_description
        }
        ]
    response = requests.post(
        url,
        json={"model": "llama3.1:latest", "messages": messages, "stream": False}
    )
    return response.json()


def greet(name: str) -> str:
    return f"Cześć, {name}"

if __name__ == "__main__":
    print(chat("Cześć, kim jesteś?"))