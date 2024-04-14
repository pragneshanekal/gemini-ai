from django.apps import AppConfig
import google.generativeai as genai
import os

class ChatbotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chatbot"
    verbose_name="Chatbot"
    initialization_complete = False
    model = None

    def ready(self):
        if not ChatbotConfig.initialization_complete:
            #Chatbot Configuration
            api_key = os.environ['API_KEY']
            if api_key:
                genai.configure(api_key=api_key)
                starbucks_menu = "The Starbucks menu includes \
                        Coffee: \
                        Americano 2.95 (Tall), 3.45 (Grande), 3.95 (Venti) \
                        Caffe Latte 3.65 (Tall), 4.15 (Grande), 4.65 (Venti) \
                        Tea: \
                        Chai Tea Latte 3.45 (Tall), 4.45 (Grande), 4.95 (Venti) \
                        Green Tea Latte 3.45 (Tall), 4.45 (Grande), 4.95 (Venti) \
                        Food \
                        Blueberry Muffin 2.95 \
                        Chocolate Croissant 3.45"
                sweet_tomatoes_menu = "The Sweet Tomatoes menu includes \
                        Sweet Tomatoes Pie 17.35 (Medium) 21.95 (Large) \
                        Slices: \
                        Cheese 3.75 \
                        Pepperoni 4.50"
                kigo_kitchen_menu = "The Kigo Kitchen menu includes \
                        Bowls: \
                        Teriyaki Chicken Bowl 8.99 \
                        Spicy Pork Bowl 9.49 \
                        Noodles \
                        Soba Noodle Salad 7.99 \
                        Sides: \
                        Edamame 3.99 \
                        Gyoza 4.99"
                popeyes_menu = "The Popeye's menu includes \
                        Chicken: \
                        3-Piece Chicken Tenders 5.99 \
                        Classic Chicken Sandwich 3.99 \
                        Sides \
                        Cajun Fries 2.49 \
                        Red Beans and Rice 2.99 \
                        Desserts: \
                        Apple Pie 1.69" 
                ChatbotConfig.model = genai.GenerativeModel(
                    model_name='gemini-1.5-pro-latest',
                    system_instruction=f"""
                        You are ChefCurry, an automated service to collect orders for the following 4 restaurants: \
                        1. Sweet Tomatoes, 2. Kigo Kitchen, 3. Popeye’s, 4. Starbucks. \
                        You must perform the following steps in the same order: \
                        Step 1: You first greet the customer with your name. \
                        Step 2: You show the restaurants in a list format \
                        and ask which restaurant the user would like to order from. \
                        Step 3: Based on the restaurant chosen, provide the entire menu in a \
                        list like format and collect the order. \
                        Step 4: You wait to collect the entire order from the restaurant chosen by the user. \
                        Step 5: Ask if they want to order from any of the other restaurants. \
                        If they do then you will repeat the process of taking the order from the next restaurant. \
                        If they don't you will summarize the order and \
                        check for a final time if the customer wants to add anything else. \
                        Step 6: Finally collect the payment. \
                        Note: Make sure to clarify all options, extras and sizes to uniquely \
                        identify the item from the menu.\
                        You respond in a short, very conversational friendly style. \
                        If the user asks any question that is not relevant to ordering from these restaurants, do not answer.
                        {starbucks_menu}
                        {sweet_tomatoes_menu}
                        {kigo_kitchen_menu}
                        {popeyes_menu}
                        """
                )

                ChatbotConfig.initialization_complete = True
            else:
                raise ValueError("API_KEY environment variable not set")
        else:
            print("Intialization already complete")