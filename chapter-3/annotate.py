#store customer messages
messages = [
    "I want a refund for my order",
    "My package arrived today",
    "Can I get a refund?",
    "The product is damaged",
    "I need help with my account",
    "Please process my refund",
    "Where is my delivery?",
    "I was charged twice",
    "How long does a refund take?",
    "Thank you for your help"
]

refund_count = 0

#take each message from the message list
for message in messages:
#check if the message contains the word refund
    if "refund" in message.lower():
        print(message)
        refund_count = refund_count + 1

print("Total refund messages:", refund_count) 