import os
import tensorflow as tf

from src.classes.ParameterOptimization import ParameterOptimization
from src.classes.Experiment import Experiment
from src.utils.generate_reports import generate_tables, generate_graphs, generate_graph_experiment

# Set TensorFlow to use only CPU
tf.config.set_visible_devices([], 'GPU')

def run_parameter_optimization(data, name, models, imputation_methods, iterations_sampler):
    print('[INFO] RUNNING PARAMETER OPTIMIZATION]')
    optimization = ParameterOptimization(data, name, models, imputation_methods, iterations_sampler, device='cpu')
    optimization.run()
    print('[INFO] PARAMETER OPTIMIZATION FINISHED')

    data_path = f'../results/{data}/{name}'

    print('[INFO] GENERATING REPORT')
    generate_tables(data_path)
    generate_graphs(data_path)
    print('[INFO] REPORT GENERATED')


def main(data, name, models, imputation_methods, iterations_sampler, hours_before_onset):
    data_path = f'./results/{data}/{name}'

    if not os.path.exists(data_path):
        run_parameter_optimization(data, name, models, imputation_methods, iterations_sampler)

    print('[INFO] STARTING EXPERIMENT')
    experiment = Experiment(data, name, hours_before_onset, device='cpu')
    experiment.run()
    print('[INFO] EXPERIMENT FINISHED')

    print('[INFO] GENERATING REPORT')
    generate_graph_experiment(data_path)
    print('[INFO] REPORT GENERATED')

    print('[INFO] EXECUTION FINISHED')


if __name__ == '__main__':
    name = 'name_experiment'

    hours_before_onset = 7

    iterations_sampler = 25

    # Mark the chosen ones with 1, others with 0

    imputation_methods = {
        'carry_forward': 1,
        'forward_filling': 1,
        'zero_imputation': 1,
        'linear_interpolation': 1,
        'indicator_imputation': 1,
    }

    models = {
        'TCN': 0,
        'CNN': 1,
        'MLP': 1,
        'GRU': 0,
        'LSTM': 0,
        'LinearSVC': 0,
        'XGBClassifier': 1,
        'LogisticRegression': 0,
        'AdaBoostClassifier': 0,
        'RandomForestClassifier': 0
    }

    # Specify the path to your dataset
    data = '/Users/lola/Nutstore/Harvard/Capstone/sepsis-review/data/sepsis.csv'

    main(data, name, models, imputation_methods, iterations_sampler, hours_before_onset)
