import numpy as np
import pandas as pd
import pytest
from src.naive_bayes_classifier import *


@pytest.fixture
def default_conditional_probabilities():
    obs = DEFAULT_OBSERVATIONS
    return calculate_conditional_probabilities(obs)


def test_conditional_probabilities_is_pandas_dataframe(default_conditional_probabilities):
    assert isinstance(default_conditional_probabilities, pd.DataFrame)


def test_conditional_probabilities_has_at_least_one_building_class_and_attribute(default_conditional_probabilities):
    assert default_conditional_probabilities.shape[0] >= 1
    # class_id + (attributes)
    assert default_conditional_probabilities.shape[1] >= 2


def test_conditional_probabilities_are_probabilities(default_conditional_probabilities):
    for attribute in default_conditional_probabilities:
        if attribute in ['class_id', 'count']:
            continue
        p = default_conditional_probabilities[attribute]
        assert (0 <= p).all() and (p <= 1).all()


@pytest.fixture
def default_classifier():
    nbc = NaiveBayesClassifier()
    nbc.conditional_probabilities = calculate_conditional_probabilities(
        DEFAULT_OBSERVATIONS)
    nbc.prior = np.ones(nbc.conditional_probabilities.shape[0])
    return nbc


def test_calculate_posterior_normalizes_probabilities_by_default(default_classifier):
    res = default_classifier.calculate_posterior(["1"], ["yes"])
    assert np.isclose(res['posterior'].sum(), 1.0)
    res = default_classifier.calculate_posterior(["1"], ["no"])
    assert np.isclose(res['posterior'].sum(), 1.0)
    res = default_classifier.calculate_posterior(["1"], ["skip"])
    assert np.isclose(res['posterior'].sum(), 1.0)


def test_calculate_posterior_unnormalized_probabilities_are_probabilities(default_classifier):
    res_true = default_classifier.calculate_posterior(
        ["1"], ["yes"], normalize=False)
    assert (0 <= res_true['posterior']).all() and (
        res_true['posterior'] <= 1).all()
    res_false = default_classifier.calculate_posterior(
        ["1"], ["no"], normalize=False)
    assert (0 <= res_false['posterior']).all() and (
        res_false['posterior'] <= 1).all()
    res_false = default_classifier.calculate_posterior(
        ["1"], ["skip"], normalize=False)
    assert (0 <= res_false['posterior']).all() and (
        res_false['posterior'] == 1).all()


def test_calculate_posterior_unnormalized_probabilities_are_bernoulli(default_classifier):
    res_true = default_classifier.calculate_posterior(
        ["1"], ["yes"], normalize=False)
    res_false = default_classifier.calculate_posterior(
        ["1"], ["no"], normalize=False)
    print(default_classifier.conditional_probabilities)
    print(res_true)
    print(res_false)
    print(res_true['posterior'] + res_false['posterior'])
    assert np.isclose(res_true['posterior'] +
                      res_false['posterior'], 1.0).all()


def test_skip_returns_prior_in_calculate_posterior(default_classifier):
    # Generate a deterministic but random prior
    n_attributes = len(
        default_classifier.conditional_probabilities.columns) - 1
    np.random.seed(12345)
    prior = np.random.permutation(n_attributes).astype(float)
    prior /= prior.sum()

    # Calculate the posterior and check that it's equal to the prior
    res_skip = default_classifier.calculate_posterior(
        ["1"], ["skip"], prior=prior)
    assert np.isclose(prior, res_skip['posterior']).all()
