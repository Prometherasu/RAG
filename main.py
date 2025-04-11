from app.pipeline import pipeline, init
from app.index_elastic import delete_index
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
#model = None
def main():
    delete_index()
    exit = False
    first = True
    while not exit:
        if first:
            init(model)
            first = False

        query = input("Pose ta question :\n> ")
        if query == "exit":
            exit = True
        else:
            pipeline(query, model)


if __name__ == "__main__":
    main()
