import pandas as pd
from optimal_model import optimal_model
from generate_combinations import generate_combinations
from multiprocessing import cpu_count, current_process, Manager, Process
import os
import time
from collections import Counter

def consumer_task(q, list_of_models):

    while not q.empty():
        value = q.get(block=True, timeout=0.05)

        best_model = optimal_model(df=value)

        list_of_models.append(best_model)

        print(f"consumer {current_process().name} (PID = {os.getpid()}) getting value from queue")



if __name__ == '__main__':

    df = pd.read_csv('data.csv')

    manager = Manager()
    df_subsets = manager.Queue()
    list_of_models = manager.list()

    # Generate a list of dataframes with different combinations of variables
    list_of_dfs = generate_combinations(df=df, k=3, m=500)

    for df_subset in list_of_dfs:
        df_subsets.put(df_subset)

    start_time = time.time()

    consumer_list = []
    for i in range(cpu_count()):
        consumer = Process(target=consumer_task, args=(df_subsets,list_of_models))
        consumer.start()
        consumer_list.append(consumer)

    [consumer.join() for consumer in consumer_list]

    # print(f"--- {time.time() - start_time} seconds ---")

    accuracy = 0
    max_accuracy = 0
    best_model = None

    for model in list_of_models:
        accuracy += model.accuracy()
        if model.accuracy() > max_accuracy:
            max_accuracy = model.accuracy()
            best_model = model

    print(f"\nAverage Accuracy: {accuracy/len(list_of_models)}")
    print(f"Best Performing Model Accuracy: {max_accuracy}")

    test_df = pd.read_csv('testing_data.csv')

    variables_to_drop = list((Counter(test_df.columns.values.tolist()) - Counter(best_model.columns)).elements())

    test_df = test_df.drop(variables_to_drop, axis=1)

    coefficients = zip(list(test_df.drop(['votes', 'player_id'], axis=1).columns), best_model.ml.coef_)
    print(f"\nCoeff: {list(coefficients)}\n")


    for index, row in test_df.iterrows():
        my_list = [row[value] for value in test_df.columns.values.tolist()]

        player_id = my_list[0]
        actual_votes = int(my_list[1])

        predicted_votes = int(best_model.ml.predict([my_list[2:]])[0])

        print(f"Player ID: {player_id} --- Actual/Predicted Votes: {actual_votes}/{predicted_votes}")



