import chromadb

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="railcard_collection")

# Define railcards and their corresponding inputs
railcards = {
    "TSU": [
        "16-17 Saver",
        "TSU railcard",
    ],
    "YNG": [
        "16-25 Railcard",
        "YNG railcard",
    ],
    "TST": [
        "26-30 Railcard",
        "TST railcard",
    ],
    "NGC": [
        "annual gold card",
        "ngc railcard",
    ],
    "DRD": [
        "dales railcard",
        "drd railcard",
    ],
    "DCG": [
        "devon & cornwall gold card",
        "devon and cornwall gold card"
        "dcg railcard",
    ],
    "DCR": [
        "devon & cornwall card",
        "devon and cornwall card"
        "dcr railcard",
    ],
    "DIS": [
        "disabled persons railcard",
        "dis railcard",
    ],
    "EVC": [
        "esk valley railcard",
        "evc railcard",
    ],
    "FAM": [
        "family & friends railcard",
        "fam railcard",
    ],
    "GS3": [
        "group save railcard",
        "GS3 railcard",
    ],
    "HRC": [
        "highland railcard",
        "hrc railcard",
    ],
    "HMF": [
        "hm forces railcard",
        "hmf railcard",
    ],
    "JCP": [
        "job centre plus travel discount card",
        "hrc railcard",
    ],
    "CUR": [
        "my cumbria card",
        "mycumbria card",
        "cur railcard",
    ]
}


# Add inputs to collection with corresponding IDs
for railcard, inputs in railcards.items():
    ids = [f"{railcard}_{i}" for i in range(len(inputs))]
    collection.add(
        documents=inputs,
        ids=ids
    )


def get_railcard(user_input):
    results = collection.query(
        query_texts=[user_input],
        n_results=1
    )

    # Extracting IDs from results
    ids = results["ids"][0]

    # If IDs is returned as a list, extract railcard from the first ID
    if isinstance(ids, list):
        railcard = ids[0].split("_")[0]
    else:
        railcard = ids.split("_")[0]

    return railcard

