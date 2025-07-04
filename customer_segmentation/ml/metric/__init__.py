from sklearn.metrics import (confusion_matrix, f1_score, precision_score,
                             recall_score)

from customer_segmentation.entity.artifact_entity import ClassificationMetricArtifact


def calculate_metric(model, x, y) -> ClassificationMetricArtifact:
    """
    model: estimator
    x: input feature
    y: output feature
    """
    yhat = model.predict(x)
    classification_metric = ClassificationMetricArtifact(
        f1_score=f1_score(y, yhat, average='weighted'),
        recall_score=recall_score(y, yhat, average='weighted'),
        precision_score=precision_score(y, yhat, average='weighted'),
    )
    return classification_metric


def total_cost(y_true, y_pred):
    """
    This function takes y_ture, y_predicted, and prints Total cost due to misclassification
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    cost = 10 * fp + 500 * fn
    return cost
