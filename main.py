from app.pipeline import pipeline, init
from app.index_elastic import delete_index

def main():
    #delete_index()
    exit = False
    first = True
    while not exit:
        if first:
            init()
            first = False

        query = input("Pose ta question :\n> ")
        if query == "exit":
            exit = True
        else:
            pipeline(query)


if __name__ == "__main__":
    main()
