import yaml

with open('config\model.yaml','rb') as yaml_obj:
    data = yaml.safe_load(yaml_obj)

    print(data['models']['logistic']['hyperparameters'])


