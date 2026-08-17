from utils.analyser import understand_question

columns = [
    "price",
    "quantity",
    "category",
    "customer_id"
]

question = input("Ask a question: ")

result = understand_question(question, columns)

print(result)