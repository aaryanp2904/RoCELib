from datasets.ExampleDatasets import get_example_dataset
from models.pytorch_models.SimpleNNModel import SimpleNNModel
from recourse_methods.RNCE import RNCE
from tasks.ClassificationTask import ClassificationTask


def test_rnce() -> None:
    model = SimpleNNModel(34, [8], 1)
    dl = get_example_dataset("ionosphere")

    ct = ClassificationTask(model, dl)

    dl.default_preprocess()
    ct.train()

    delta = 0.01

    recourse = RNCE(ct, delta)

    _, neg = list(dl.get_negative_instances(neg_value=0).iterrows())[0]

    for _, neg in dl.get_negative_instances(neg_value=0).head(10).iterrows():

        res = recourse.generate_for_instance(neg)

        print(res)

        assert recourse.intabs.evaluate(res, delta=delta)
