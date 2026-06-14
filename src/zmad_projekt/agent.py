import json
import sys
from pathlib import Path
from dotenv import load_dotenv
from pydantic_ai import Agent


#from zmad_projekt import functions
try:
	from zmad_projekt.tools import calculate_stress, predict_survival_on_titanic, convert_temp, predict_concrete_compressive_strength
except ModuleNotFoundError:
	# Allow running this file directly from inside the package folder.
	project_root = Path(__file__).resolve().parents[1]
	if str(project_root) not in sys.path:
		sys.path.insert(0, str(project_root))
	from zmad_projekt.tools import calculate_stress, predict_survival_on_titanic, convert_temp, predict_concrete_compressive_strength

load_dotenv()

agent = Agent(  
'ollama:qwen3.5:2b',
instructions='Be concise, reply with one sentence.',  
model_settings={'thinking':False},
tools = [calculate_stress, convert_temp, predict_survival_on_titanic, predict_concrete_compressive_strength] # TO jest równoważne @agent.tool_plain ... itd
)

#Dodanie narzędzia do agenta

# @agent.tool_plain
# async def calculate_stress(f: float, A: float):
#     """This function is used to calculate stress

#     """
#     try:
#         return functions.calculate_stress(f,A)
#     except Exception as e:
#         return f"There was an error: {e}"


result1 = agent.run_sync('What is the value of stress for 100 N and 100 mm^2 of the area?')  
result2 = agent.run_sync('Convert 100 Celsius to Fahrenheit')
result3 = agent.run_sync('Would a 25 man with a fare of 50 and no siblings or parents on board survive the Titanic?')
result4 = agent.run_sync('What is the compressive strength of concrete with cement content = 50 kg/m^3, blast furnace slag = 50 kg/m^3, fly ash = 50 kg/m^3, and water content = 12 kg/m^3, superplasticizer = 50 kg/m^3, coarse aggregate = 150 kg/m^3, fine aggregate = 200 kg/m^3, and age = 15 days?')
print("Agent responses:")
print("\n" + result1.output)
print("\n" + result2.output)
print("\n" + result3.output)
print("\n" + result4.output)
