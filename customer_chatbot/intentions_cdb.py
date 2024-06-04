import chromadb

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="my_collection")

# Define intentions and their corresponding inputs
intentions = {
    "booking": [
        "How can I make a reservation?",
        "I'd like to book a ticket.",
        "Can I reserve a seat on the next train?",
        "Book me a seat for tomorrow's journey.",
        "How do I make a booking?"
        "Book a train from to"
        "I want a ticket from to"
        "Price for passengers to"
        "Book a train from place to place on the day of month"
    ],
    "delay": [
        "Is the train running late?",
        "What's the delay on train #123?",
        "Has the train been delayed?",
        "Why is the train delayed?",
        "When will the delayed train arrive?"
        "How many minutes late am I?"
    ],
    "greeting": [
        "hello",
        "hi",
        "hey",
        "heya"
    ],
    "goodbye": [
        "bye",
        "quit",
        "goodbye",
        "that's all",
        "I don't need anything else",
        "I'm done"
    ],
    "thanks": [
        "thanks",
        "thank you",
        "thanks for your help",
        "I appreciate it",
    ]
}

# Add inputs to collection with corresponding IDs
for intention, inputs in intentions.items():
    ids = [f"{intention}_{i}" for i in range(len(inputs))]
    collection.add(
        documents=inputs,
        ids=ids
    )

def get_similar_intention(user_input):
    results = collection.query(
        query_texts=[user_input],
        n_results=1
    )

    # Extracting IDs from results
    ids = results["ids"][0]

    # If IDs is returned as a list, extract intention from the first ID
    if isinstance(ids, list):
        intention = ids[0].split("_")[0]
    else:
        intention = ids.split("_")[0]

    return intention

