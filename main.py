import aiFuncthions as ai

try :
    print("choose the number of heuristic we will work with")
    print("1 - Coin Parity\n"+"2 - Mobility\n"+"3 - Corner occupancy\n"+"Otherwise, we will use them all ")
    ai.heuristic_number=int(input("Enter the number : "))
    print("in main heuristic_number is ",ai.heuristic_number)
    ai.f.ai_vs_human_main_fun_gui()
except Exception as ex:
    print("erorr OTHER Exception",ex)

