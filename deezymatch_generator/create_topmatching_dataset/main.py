import pandas as pd
import utils
import os 

def main():
    wikigaz_db = "wikiGazetteer" # Name of your Wikigazetteer DB in the MySQL server
    username_db = "root" # Your MySQL user name
    password_db = "Aa123456" # Your MySQL password
    min_wikigaz = "wikigaz_en" # Output name for the minimal Wikigazetteer from which we will create a training set

    if not os.path.exists(min_wikigaz + ".pkl"):
        # Create a minimal wikigazetteer from MySQL server:
        wgdf = utils.create_minimal_gaz(wikigaz_db, username_db, password_db, min_wikigaz)
    else:
        # If you have skipped Step 1, load your own gazetteer here, updating this line as needed:
        wgdf = pd.read_pickle(min_wikigaz + ".pkl")

    # Each bounding box is a list with coordinate limits: [W, S, E, N]
    bboxes = [[-96.04, 32.96, -71.16, 45.04], # Midwest + East Coast (TX -> SW, MN -> NW, ON-CA -> NE, FL -> SE)
            [-3.42, 50.92, 1.49, 56.03]] # England + Wales

    # Filter minimal gazetteer by coordinate bounding boxes:
    wgdf = wgdf[wgdf.apply(lambda x: utils.filter_gaz_by_bbox(x["latitude"], x["longitude"], bboxes), axis=1)]

    print(wgdf.shape)

    # Create the toponym matching training dataset

    titles_per_chunk = 1000 # how many titles are processed by chunk
    kilometre_distance = 20 # minimum distance in km for negative toponym pairs (i.e.
                            # toponyms of locations closer than x km will not be selected
                            # as negative matches)
    N = "default" # Number of CPUs (default: all available CPUs)
    dataset_name = "wikigaz_en_topmatching.txt" # Name of the output file where the
                                                    # toponym matching dataset is stored

    # Create the dataset:
    utils.create_pairmatch_dataset(N, titles_per_chunk, wgdf, kilometre_distance, dataset_name)

    # View the last 20 entries of your toponym matching dataset
    pd.read_csv(dataset_name, sep="\t", names=["Toponym1", "Toponym2", "Matching"]).tail(20)

if __name__ == '__main__':
    main()