from utils.analyser import understand_question

columns = [
    "category",
    "sales",
    "price",
    "quantity"
]

question = input("Ask a question: ")

result = understand_question(question, columns)

print(result)