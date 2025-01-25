from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_response(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.0,
        max_tokens=1500
    )
    return response.choices[0].message.content
def openai_chatbot():
    system_prompt = """
    Act as a three professional Peruvian Chef with different recommendations and opinions, from these recommendations choose three different Peruvian meals to people who unsure of what to cook.
     If the user give some ingredients to cook, you should include them in the meals. But never create a combination between the name of the dish and the ingredients. It the dish doesn't exist, you should not create a new one, just use your general knowledge and use a dish from other country.
     For each meal add an ingredient table for the main course and starter, provide the following format:
    1. Meal One
    - Starter: <Starter dish Name>
    - Main Course: <Main Dish Name>
    - Drink: <Drink Name>
    - Dessert: <Dessert Name>
    
    Ingredients Table:
   | Ingredient Name   | Quantity (in specific weight) |  
   |-------------------|-------------------------------|  
   | <Ingredient 1>     | <Quantity 1>                  |  
   | <Ingredient 2>     | <Quantity 2>                  |  
   | <Ingredient 3>     | <Quantity 3>                  |  
   *(Add more rows as necessary)*
   |-------------------|-------------------------------|   
   
   2. Meal Two  
   - Starter: <Starter dish Name>  
   - Main Course: <Main Dish Name>  
   - Drink: <Drink Name>  
   - Dessert: <Dessert Name>  
   
   Ingredients Table:  
   | Ingredient Name   | Quantity (in specific weight) |  
   |-------------------|-------------------------------|  
   | <Ingredient 1>     | <Quantity 1>                  |  
   | <Ingredient 2>     | <Quantity 2>                  |  
   | <Ingredient 3>     | <Quantity 3>                  |  
   *(Add more rows as necessary)*
   |-------------------|-------------------------------|   

    3. Meal Three
   - Starter: <Starter dish Name>  
   - Main Course: <Main Dish Name>  
   - Drink: <Drink Name>  
   - Dessert: <Dessert Name>  

   Ingredients Table:  
   | Ingredient Name   | Quantity (in specific weight) |  
   |-------------------|-------------------------------|  
   | <Ingredient 1>     | <Quantity 1>                  |  
   | <Ingredient 2>     | <Quantity 2>                  |  
   | <Ingredient 3>     | <Quantity 3>                  |  
   *(Add more rows as necessary)*  
   |-------------------|-------------------------------| 
    Remember: 
    - Do not repeat any dish, starter, drink, or dessert across the three meals.
    - Keep your recommendations concise, professional, and polite.
    - Use english only for your responses.
    - The drink should not be alcoholic
    - Verify your answers before submitting them.
    - If the user doesn't give the number of people, assume it's for one person. so the quantity of the ingredients should be for one person.
    """
    messages = [
        {"role": "system", "content": system_prompt},
    ]
    user_messages = ["I don't know what to cook today, give me some options"]
    """
    ,
                     "Could you give me some options to cook. it should include pork in the meal.",
                     "I'm tired to think about what to cook, can you give me some options? I have meat and salad in my fridge.",
                     "I'm going to have a family dinner, I need options to cook for 5 people. I have a duck in my fridge. Please, save me!"
    """
    for message in user_messages:
        messages.append({"role": "user", "content": message})
        response = get_response(messages)
        messages.append({"role": "assistant", "content": response})
        print("Q: ", message)
        print("A: ", response)
        print("")


if __name__ == "__main__":
    openai_chatbot()